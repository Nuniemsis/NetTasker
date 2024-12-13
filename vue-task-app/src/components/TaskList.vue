<template>
    <ul class="list-group">
      <li
        v-for="task in tasks"
        :key="task.task_id"
        class="list-group-item d-flex justify-content-between align-items-center"
        :class="{
          'list-group-item-success': task.status === 'completed',
          'list-group-item-warning': task.status === 'pending',
          'list-group-item-danger': task.status === 'failed',
        }"
      >
        <span class="text-truncate" style="max-width: 60%;">{{ task.task_id }}</span>
        <span class="badge bg-secondary">{{ task.status }}</span>
      </li>
    </ul>
  </template>
  
  <script>
  export default {
    name: "TaskList",
    props: ["tasks"], // Recibe la lista de tareas como prop
  };
  </script>
  