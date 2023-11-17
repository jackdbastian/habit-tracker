<script>
  import { currentUser, pb } from '$lib/auth_store';

  let username;
  let password;
  let errorMessage = '';
  let trackData;

  async function login() {
    try{
      const user = await pb.collection('users').authWithPassword(username, password);
      console.log(user)
    } catch (err) {
      errorMessage = 'Login Failed';
    }
  }

  async function signUp() {
    try {
      const data = {
          "username": username,
          "password": password,
          "passwordConfirm": password,
      };
      const createdUser = await pb.collection('users').create(data);
      await login();
    } catch (err) {
      errorMessage = 'Sign Up Failed';
    }
  }

  function signOut() {
    pb.authStore.clear();
  }

</script>

{#if $currentUser}
  <p>
    Signed in as {$currentUser.username} 
    {trackData}
    <button on:click={signOut}>Sign Out</button>
  </p>
{:else}
<div class="parent">
  <div class="login">
    <form on:submit|preventDefault>
      <input
        placeholder="Username"
        type="text"
        bind:value={username}
      />

      <input 
        placeholder="Password" 
        type="password" 
        bind:value={password} 
      />
      <p>{errorMessage}</p>

      <button on:click={login}>Login</button>
      <button on:click={signUp}>Sign Up</button>
    </form>
  </div>
</div>
{/if}

<style>
  .parent {
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .login {
    margin: 0 auto;
  }
</style>
  