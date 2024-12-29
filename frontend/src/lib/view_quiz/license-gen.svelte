<script lang="ts">
	import { fade } from 'svelte/transition';
    import Spinner from '$lib/Spinner.svelte';
	import { onMount } from 'svelte';
    import { writable } from 'svelte/store';

    export let quiz_id;
    let username = '';
    let loading = false;

    const error_message = writable('');
    const username_write = writable('');
    const license_key = writable('');

    function ClearError(event) {
		const value = event.target.value;
		username_write.set(value);
		if (value) {
			error_message.set('');
		}
	}

	const on_parent_click = (e: Event) => {
		if (e.target !== e.currentTarget) {
			return;
		}
		quiz_id = null;
	};
	const close_license_if_esc_is_pressed = (key: KeyboardEvent) => {
		if (key.code === 'Escape') {
			quiz_id = null;
		}
	};
    onMount(() => {
		document.body.addEventListener('keydown', close_license_if_esc_is_pressed);
	});


	type UserList = string[];
    
	const GetUserList = async (): Promise<UserList> => {
		const response = await fetch('/api/v1/users/list', {
			method: 'GET',
			headers: {
				'Content-Type': 'application/json'
			}
		});
		if (response.status === 200) {
			return await response.json();
		} else {
			window.location.assign('/');
		}
	};

    const CheckIfUserExists = async (username: string): Promise<boolean> => {
        try {
            const userList = await GetUserList();
            return userList.includes(username);
        } catch (error) {
            console.error('Error fetching user list:', error);
            return false;
        }
    };

    const licentie_krijgen = async (quiz_id: string, username: string) => {
        let res;
        loading = true;

        res = await fetch(
				`/api/v1/quiz/license/${quiz_id}?username=${username}`,
				{
					method: 'POST'
				}
			);
        
        if (res.status === 403) {
			alert('Je moet een administrator zijn om dit te kunnen doen!');
			window.location.assign('/dashboard');
		} else if (res.status !== 200) {
            alert('Licentie Genereren mislukt!');
			window.location.assign('/dashboard-admin');
        } else {
			const data = await res.json();
            license_key.set(data.license_key)
		}

        loading = false;
    };



    function copyToClipboard() {
        navigator.clipboard.writeText($license_key)
            .then(() => {
                alert("License key gekopieerd naar plakbord.");
            })
            .catch(err => {
                console.error("Failed to copy: ", err);
            });
        }

</script>

{#if quiz_id}
    <div class="fixed w-full h-full top-0 flex bg-black bg-opacity-50 z-50"
        on:click={on_parent_click}
        transition:fade|local={{ duration: 100 }}>
        <div class="m-auto bg-gray-600 rounded shadow-2xl flex p-4 flex-col lg:w-1/3 w-11/12 h-1/2">
            <h1 class="text-center text-4xl text-white">Licentie Key Genereren</h1>

            <div class="flex justify-center items-center my-auto">
				<label class="mr-4 font-bold text-white" style="font-size: 16px;">Username:</label>
				<input
					bind:value={username}
                    on:input={ClearError}
					class="rounded-lg p-2 outline-none placeholder:italic text-black"
					placeholder="Username"
					style="width: 50%"
				/>
			</div>

            {#if $license_key }
                <div class="flex justify-center w-full my-auto flex-col">
                    <p class="font-bold mx-auto text-white" style="font-size: 16px;">↓ Licentie/Quiz Key ↓ (Klik om te kopiëren)</p>
                    <p class="font-bold mx-auto custom-bright-red my-auto cursor-pointer" style="font-size: 14px; word-break: break-all;" on:click={copyToClipboard}>{$license_key}</p>
                </div>
		    {/if}

            {#if $error_message }
                <div class="flex justify-center w-full mt-auto">
                    <p class="text-red-600 underline" style="font-size: 16px;">{$error_message}</p>
                </div>
		    {/if}
            
            <button
                class="mt-auto mx-auto p-4 rounded-lg shadow-lg transition-all text-2xl orange-red-button"
                on:click={async () => {
                    if (!$username_write) {
                        error_message.set('Je moet een username invullen.');
                    } else {

                        const userExists = await CheckIfUserExists($username_write);
                        if (!userExists) {
                            error_message.set('Gebruiker niet gevonden.');
                        } else {
                            licentie_krijgen(quiz_id, username);
                        }

                    }
                }}>

                {#if loading}
                    <Spinner my_20={false} />
                {:else}
                    Genereer Licentie
                {/if}
		    </button>

        </div>

    </div>
{/if}