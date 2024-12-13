<template>
    <div class="text-center mb-4">
      <h1>Task Manager</h1>
      <button class="btn btn-primary btn-lg px-4" @click="createTask">
        <i class="fas fa-plus-circle me-2"></i> Create Task
      </button>
    </div>
  </template>
  
  <script>
  export default {
    name: "HeaderComponent",
    props: ["createTask"], // La función createTask se pasa como prop
  };
  </script>
  