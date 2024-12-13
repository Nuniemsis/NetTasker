<template>
    <div class="d-flex justify-content-center mt-4">
      <button
        class="btn btn-primary me-2"
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        Previous
      </button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button
        class="btn btn-primary ms-2"
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        Next
      </button>
    </div>
  </template>
  
  <script>
  export default {
    name: "PaginationControls",
    props: ["currentPage", "totalPages"], // Recibe la página actual y el total de páginas
    methods: {
      changePage(page) {
        this.$emit("page-change", page); // Emite un evento cuando se cambia la página
      },
    },
  };
  </script>
  