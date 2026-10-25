<template>
    <main class="password-reset-unavailable">
        <h1>Password reset unavailable</h1>
        <p>Email password reset is unavailable. Please contact your administrator.</p>
        <RouterLink to="/login">Return to sign in</RouterLink>
    </main>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.password-reset-unavailable {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px;
    color: var(--text-color--primary);
}
</style>
