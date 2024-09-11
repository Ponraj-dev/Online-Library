<!-- eslint-disable prettier/prettier -->
<template>
    <div class="downloads">
        <p> Update Will soon   ツ </p>
    </div>
</template>
<!-- eslint-disable prettier/prettier -->

<script>
export default {
    data() {
    },
    name: "downloads",
    methods: {
    },
    created() {
        this.fetchUsers();
    },
};
</script>
<!-- eslint-disable prettier/prettier -->
<style scoped>
.downloads{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width:100%;
    font-size: 100px;
    font-weight: bold;
    color:white;
    padding: 40px;

}

</style>