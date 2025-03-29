# SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)
#
# SPDX-License-Identifier: MPL-2.0


import json
import random
import re
import uuid
from datetime import datetime
from random import randint

import ormar.exceptions

from classquiz.helpers import generate_spreadsheet, handle_import_from_excel
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import ValidationError, BaseModel

from classquiz.auth import get_current_user
from classquiz.config import redis, settings, storage, meilisearch, license_api_user, license_api_pass, webshop_api_user, webshop_api_pass
from classquiz.db.models import Quiz, User, PlayGame, GameInLobby, QuizQuestion, QuizQuestionType
from classquiz.helpers.box_controller import generate_code
from classquiz.kahoot_importer.import_quiz import import_quiz
from uuid import UUID
import urllib.parse

from cryptography.fernet import Fernet, InvalidToken

import requests 
from requests.auth import HTTPBasicAuth

settings = settings()

router = APIRouter()

"""
class QuizGetModel(Quiz.get_pydantic(exclude={"quiz_license_key"})):
    id: uuid.UUID
    public: bool
    title: str
    description: Optional[str] = None
    user_id: uuid.UUID
    questions: list
    imported_from_kahoot: bool
    cover_image: str
    background_color: str
    background_image: str
"""

@router.get("/get/{quiz_id}")
async def get_quiz_from_id(quiz_id: str, user: User | None = Depends(get_current_user)):
    try:
        quiz_id = uuid.UUID(quiz_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="badly formed quiz id")
    
    if user is None:
        return JSONResponse(status_code=404, content={"detail": "user not found"})
    else:
        quiz = await Quiz.objects.get_or_none(id=quiz_id, user_id=user.id)

    if quiz is None:
        return JSONResponse(status_code=404, content={"detail": "quiz not found"})
    else:
        return quiz.to_dict(exclude_fields=["quiz_license_key"])


class PublicQuizResponseUser(BaseModel):
    username: str
    id: uuid.UUID

"""
class PublicQuizResponse(Quiz.get_pydantic(exclude={"questions"})):
    user_id: PublicQuizResponseUser
    questions: list[QuizQuestion]
    likes: int
    dislikes: int
    views: int
    plays: int
"""
    
class PublicInfoQuizResponse(Quiz.get_pydantic(exclude={"questions","background_color","background_image", "quiz_license_key"})):
    user_id: PublicQuizResponseUser
    likes: int
    dislikes: int
    views: int
    plays: int
    question_count: int
    
@router.get("/get/public/info/{quiz_id}",)
async def get_public_info_quiz(quiz_id: uuid.UUID):
    quiz = await Quiz.objects.select_related("user_id").get_or_none(id=quiz_id)
    if quiz is None:
        return JSONResponse(status_code=404, content={"detail": "quiz not found"})
    else:
        question_count = len(quiz.questions) if quiz.questions else 0

        quiz.views += 1
        await quiz.update()
        return PublicInfoQuizResponse(**quiz.dict(), question_count=question_count)
    
"""
@router.get("/get/public/{quiz_id}")
async def get_public_quiz(quiz_id: uuid.UUID):
    quiz = await Quiz.objects.select_related("user_id").get_or_none(id=quiz_id)
    if quiz is None:
        return JSONResponse(status_code=404, content={"detail": "quiz not found"})
    else:
        return PublicQuizResponse(**quiz.dict())
"""

"""
This code is no longer being used
@router.post("/license/{quiz_id}")
async def license_gen_quiz(
    quiz_id: str,
    username: str,
    user: User = Depends(get_current_user),
):
    if not user.admin_user:
        raise HTTPException(status_code=403, detail="Only admins are allowed to do this")
    
    try:
        quiz_id = uuid.UUID(quiz_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="badly formed quiz id")
    
    quiz = await Quiz.objects.get_or_none(id=quiz_id, user_id=user.id)
    if quiz is None:
        quiz = await Quiz.objects.get_or_none(id=quiz_id, public=True)
        if quiz is None:
            return JSONResponse(status_code=404, content={"detail": "quiz not found"})
        
    user_input = await User.objects.get_or_none(username=username)
    if user_input is None:
        return JSONResponse(status_code=404, content={"detail": "user not found"})
    
    message = user_input.user_license_key
    key = quiz.quiz_license_key

    fernet = Fernet(key)

    license = fernet.encrypt(message.encode())
    
    return {"license_key": license}
"""


@router.post("/start/{quiz_id}")
async def start_quiz(
    quiz_id: str,
    game_mode: str,
    license: str,
    request: Request,
    captcha_enabled: bool = True,
    custom_field: str | None = None,
    cqcs_enabled: bool = False,
    randomize_answers: bool = False,
    user: User = Depends(get_current_user),
):
    quiz_id_str = quiz_id
    try:
        quiz_id = uuid.UUID(quiz_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="badly formed quiz id")
    quiz = await Quiz.objects.get_or_none(id=quiz_id, user_id=user.id)
    
    if quiz is None:
        quiz = await Quiz.objects.get_or_none(id=quiz_id, public=True)
        if quiz is None:
            quiz = await Quiz.objects.get_or_none(id=quiz_id, public=False)
            if quiz is None:
                return JSONResponse(status_code=403, content={"detail": "Quiz niet gevonden."})
            elif not user.admin_user:
                return JSONResponse(status_code=403, content={"detail": "De quiz is niet openbaar."})
        
    #licentie check
    if (not user.admin_user):
        if not license: #lege string, geen license
            return JSONResponse(status_code=403, content={"detail": "Gelieve een licentie code in te vullen."})
        
        try:
            user_ip_forwarded = request.headers.get("X-Forwarded-For", request.client.host)
            user_ip_connecting = request.headers.get("CF-Connecting-IP", request.client.host)
        except Exception as error:
            print("Error IP:", error)


        #api request license check L-100
        license_check = requests.get(f'https://footballislife.be/wp-json/lmfwc/v2/licenses/{license}',
            auth = HTTPBasicAuth(license_api_user, license_api_pass))
        
        #data verzamelen uit request
        json_license_check = license_check.json()
        print("License Check:", json_license_check)
        license_status_code = json_license_check.get('data', {}).get('status')
        license_times_activated = json_license_check.get('data', {}).get('timesActivated')
        license_times_activated_max = json_license_check.get('data', {}).get('timesActivatedMax')

        if license_times_activated == None:
            license_times_activated = 0

        #errors en fouten filteren
        if license_status_code == 404:
            return JSONResponse(status_code=403, content={"detail": "De ingevoerde licentie code is ongeldig. Error: 404 License Not Found"})
        elif license_status_code == 4:
            return JSONResponse(status_code=403, content={"detail": "Deze licentie code is gedeactiveerd. Neem contact met ons op. Error: L-102 License Disabled"})
        elif license_status_code not in [2, 3]:
            return JSONResponse(status_code=403, content={"detail": "Er is een probleem opgetreden bij de status controle van de licentie. Error: L-1023 Wrong License Status"})
        elif license_times_activated_max <= license_times_activated:
            return JSONResponse(status_code=403, content={"detail": "De licentie heeft de maximale aantal speelbeurten bereikt. Error: L-104 Max Activation Reached"})
        
        if not json_license_check.get('success'):
            return JSONResponse(status_code=403, content={"detail": "Er is een probleem opgetreden bij de status controle van de licentie. Error: L-105 No Success "})
        
        #gelukt, license bestaat -> data verkrijgen
        license_id = json_license_check.get('data', {}).get('id')
        license_order_id = json_license_check.get('data', {}).get('orderId')
        license_product_id = json_license_check.get('data', {}).get('productId')

        if license_product_id:
            #api request wc for quiz check 200
            quiz_check = requests.get(f'https://footballislife.be/wp-json/wc/v3/products/{license_product_id}',
                auth = HTTPBasicAuth(webshop_api_user, webshop_api_pass))
            
            #data verzamelen uit request
            json_quiz_check = quiz_check.json()
            print("Quiz Check:", json_quiz_check)

            #als product niet gevonden is, error
            if "invalid_id" in json_quiz_check:
                return JSONResponse(status_code=403, content={"detail": "Er is een probleem opgetreden bij de id controle van de licentie. Error: L-201 Invalid Product ID"})
            
            #sku krijgen ne vergelijken
            sku = json_quiz_check.get('sku')
            if sku != quiz_id_str:
                return JSONResponse(status_code=403, content={"detail": "De licentie code is niet voor deze quiz bestemd. Error: L-202 Wrong Quiz ID", "sku": sku, "quiz_id_str": quiz_id_str})
        
        #enkel en alleen als er een order id is anders niet
        if license_order_id:
            #api request wc for user check
            user_check = requests.get(f'https://footballislife.be/wp-json/wc/v3/orders/{license_order_id}',
                auth = HTTPBasicAuth(webshop_api_user, webshop_api_pass))
            
            #data verzamelen & omzetten
            json_user_check = user_check.json()
            print("User Check:", json_user_check)
            found_shop_item = None
            found_username = None

            for shop_item in json_user_check['line_items']: #voor elk shop item in order
                if (shop_item['product_id'] == license_product_id) or (shop_item['variation_id'] == license_product_id): #als shop item id = shop item license
                    found_shop_item = shop_item

                    for meta in found_shop_item['meta_data']:
                        if meta['key'].lower() == 'gebruikersnaam' or meta['key'].lower() == 'username':
                            found_username = meta['value']
                            if found_username == user.username:
                                break
                                
            if found_username == None:
                return JSONResponse(status_code=403, content={"detail": "Er is een probleem opgetreden bij de gebruiker controle van de licentie. Error: L-301 No User in Order"})
            elif found_username != user.username:
                return JSONResponse(status_code=403, content={"detail": "De licentie code is niet aan uw account gekoppeld. Error: L-302 Wrong User"})
        
        #status aanpassen key naar active
        if license_status_code != 3:
            license_change_status = requests.put(f'https://footballislife.be/wp-json/lmfwc/v2/licenses/{license}', json={'status':'ACTIVE'}, auth = HTTPBasicAuth(license_api_user, license_api_pass))
            json_change_status = license_change_status.json()
            print("Status Change:", json_change_status)
            license_status_code = json_change_status.get('data', {}).get('status')

            if not json_change_status.get('success'):
                return JSONResponse(status_code=403, content={"detail": "Er is een probleem met het activeren van de licentie. Error: L-401 No Success"})
            if license_status_code != 3:
                return JSONResponse(status_code=403, content={"detail": "Er is een probleem met het activeren van de licentie. Error: L-402 No Status Change"})

        #license activeren - request
        ip_headers = {
           "X-Forwarded-For": f"IP:{user_ip_connecting}, User:{user.username}, Quiz: {quiz_id_str}" 
        }

        license_activate = requests.get(f'https://footballislife.be/wp-json/lmfwc/v2/licenses/activate/{license}', headers=ip_headers,
            auth = HTTPBasicAuth(license_api_user, license_api_pass))
        
        #data verkrijgen
        json_license_activate = license_activate.json()
        print("Activate Check:", json_license_activate)
        str_license_activate = str(json_license_activate)

        #filteren
        if "error" in str_license_activate:
            if "expired" in str_license_activate:
                license_expired_message = json_license_activate['data']['errors']['lmfwc_rest_license_expired'][0]
                date_expired = re.search(r'(\d{4}-\d{2}-\d{2})', license_expired_message)
                if date_expired:
                    date_expired = date_expired.group(0).split("-")
                    formatted_date = f"{date_expired[2]}/{date_expired[1]}/{date_expired[0]}"
                    return JSONResponse(status_code=403, content={"detail": f"De licentie is vervallen op {formatted_date}. Error: L-501 License Expired"})
                else:
                    return JSONResponse(status_code=403, content={"detail": "De licentie is vervallen. Error: L-502 License Expired, Date Unknown"})
            elif "maximum activation count" in str_license_activate:
                return JSONResponse(status_code=403, content={"detail": "De licentie heeft de maximale aantal speelbeurten bereikt. Error: L-503 Max Activation Reached"})
            else:
                return JSONResponse(status_code=403, content={"detail": "Er is een probleem met het activeren van de licentie. Error: L-504 Unknown Error in Activation"})

        """
        old license code
        key = quiz.quiz_license_key

        fernet = Fernet(key)
        try:
            decMessage = fernet.decrypt(license.encode()).decode()

            if (decMessage != user.user_license_key):
                return JSONResponse(status_code=403, content={"detail": "invalid license key"})
        except InvalidToken:
            return JSONResponse(status_code=403, content={"detail": "invalid license key"})
        """
        
    quiz.plays += 1
    await quiz.update()
    game_pin = randint(100000, 999999)
    if custom_field == "":
        custom_field = None
    game = await redis.get(f"game:{game_pin}")
    while game is not None:
        game_pin = randint(100000, 999999)
        game = await redis.get(f"game:{game_pin}")

    if randomize_answers:
        for question in quiz.questions:
            if question["type"] == QuizQuestionType.RANGE:
                continue
            if question["type"] == QuizQuestionType.SLIDE:
                continue
            random.shuffle(question["answers"])

    game = PlayGame(
        quiz_id=quiz_id,
        game_pin=str(game_pin),
        questions=quiz.questions,
        game_id=uuid.uuid4(),
        title=quiz.title,
        description=quiz.description,
        captcha_enabled=captcha_enabled,
        cover_image=quiz.cover_image,
        game_mode=game_mode,
        user_id=user.id,
        background_color=quiz.background_color,
        custom_field=custom_field,
        background_image=quiz.background_image,
    )
    code = None
    if cqcs_enabled:
        code = generate_code(6)
        await redis.set(f"game:cqc:code:{code}", game_pin, ex=3600)
    await redis.set(f"game:{str(game.game_pin)}", game.json(), ex=18000)
    await redis.set(f"game_pin:{user.id}:{quiz_id}", game_pin, ex=18000)

    await redis.set(
        f"game_in_lobby:{user.id.hex}",
        GameInLobby(game_id=game.game_id, game_pin=str(game_pin), quiz_title=quiz.title).json(),
        ex=900,
    )
    return {**quiz.dict(exclude={"id"}), **game.dict(exclude={"questions"}), "cqc_code": code}


class CheckIfCaptchaEnabledResponse(BaseModel):
    enabled: bool
    game_mode: str | None = None
    custom_field: str | None = None


@router.get("/play/check_captcha/{game_pin}", response_model=CheckIfCaptchaEnabledResponse)
async def check_if_captcha_enabled(game_pin: str):
    game = await redis.get(f"game:{game_pin}")
    if game is None:
        return JSONResponse(status_code=404, content={"detail": "game not found"})
    game = PlayGame.parse_raw(game)
    if game.captcha_enabled:
        return CheckIfCaptchaEnabledResponse(enabled=True, game_mode=game.game_mode, custom_field=game.custom_field)
    else:
        return CheckIfCaptchaEnabledResponse(enabled=False, game_mode=game.game_mode, custom_field=game.custom_field)


@router.get("/join/{game_pin}", deprecated=True)
async def get_game_id(game_pin: str):
    redis_res = await redis.get(f"game:{game_pin}")
    if redis_res is None:
        raise HTTPException(status_code=404, detail="game not found")
    else:
        return json.loads(redis_res)["game_id"]


@router.get("/list")
async def get_quiz_list(user: User = Depends(get_current_user), page_size: int | None = 10, page: int | None = 1):
    try:
        return (
            await Quiz.objects.order_by(Quiz.updated_at.desc())
            .filter(user_id=user.id)
            .paginate(page, page_size=page_size)
            .all()
        )
    except ormar.exceptions.QueryDefinitionError:
        raise HTTPException(status_code=400, detail="Invalid page(size). page(size) have to be greater than 0.")


@router.post("/import/{quiz_id}")
async def import_quiz_route(quiz_id: str, user: User = Depends(get_current_user)):
    if user.storage_used > settings.free_storage_limit:
        raise HTTPException(status_code=409, detail="Storage limit reached")
    if user.admin_user:
        resp_data = await import_quiz(quiz_id, user)
        try:
            if type(resp_data) is int:
                raise HTTPException(status_code=resp_data, detail="kahoot")
            else:
                return resp_data
        except ValidationError:
            raise HTTPException(400, detail="unsupported")
    else:
        raise HTTPException(status_code=403, detail="Only admins are allowed to do this")


@router.delete("/delete/{quiz_id}")
async def delete_quiz(quiz_id: str, user: User = Depends(get_current_user)):
    try:
        quiz_id = uuid.UUID(quiz_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="badly formed quiz id")
    quiz = await Quiz.objects.get_or_none(id=quiz_id, user_id=user.id)

    if quiz is None:
        return JSONResponse(status_code=404, content={"detail": "quiz not found"})
    pics_to_delete = []
    pic_name_regex = re.compile("^.*/(.{36}--.{36})$")
    for question in quiz.questions:
        try:
            if question["image"] is not None and not str(question["image"]).startswith("https://i.imgur.com/"):
                old_image_to_delete = pic_name_regex.match(question["image"])
                if old_image_to_delete is not None:
                    pics_to_delete.append(old_image_to_delete.group(1))
        except KeyError:
            pass
    if len(pics_to_delete) != 0:
        await storage.delete(pics_to_delete)
    meilisearch.index(settings.meilisearch_index).delete_document(str(quiz.id))
    return await quiz.delete()


@router.get("/export_data/{export_token}", response_class=StreamingResponse)
async def export_quiz_answers(export_token: str, game_pin: str):
    data = await redis.get(f"export_token:{export_token}")
    if data is None:
        raise HTTPException(status_code=404, detail="export token not found")
    data = json.loads(data)
    data2 = await redis.get(f"game:{game_pin}")
    game_data = PlayGame.parse_raw(data2)
    print(type(game_data.quiz_id))
    quiz = await Quiz.objects.get_or_none(id=UUID(game_data.quiz_id))
    if quiz is None:
        raise HTTPException(status_code=404, detail="quiz not found")

    player_fields = await redis.hgetall(f"game:{game_pin}:players:custom_fields")
    score_data = await redis.hgetall(f"game_session:{game_pin}:player_scores")
    spreadsheet = await generate_spreadsheet(
        quiz=quiz, quiz_results=data, player_fields=player_fields, player_scores=score_data
    )

    def iter_file():
        yield from spreadsheet

    await redis.delete(f"export_token:{export_token}")
    return StreamingResponse(
        iter_file(),
        media_type="application/vnd.ms-excel",
        headers={
            "Content-Disposition": f"attachment;filename=ClassQuiz-{urllib.parse.quote(quiz.title)}-{datetime.now().strftime('%m-%d-%Y')}.xlsx"  # noqa: E501
        },
    )


@router.post("/excel-import")
async def import_from_excel(file: UploadFile = File(), user: User = Depends(get_current_user)) -> Quiz:
    quiz = await handle_import_from_excel(file.file, user)
    return Quiz.parse_obj(quiz.dict(exclude={"user_id": ...}))
