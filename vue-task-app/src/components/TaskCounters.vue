<template>
    <div class="row text-center mb-4">
      <div class="col-md-4">
        <div class="card border-success">
          <div class="card-body">
            <h5 class="card-title text-success">Completed Tasks</h5>
            <h3 class="text-success">{{ completedTasks }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-warning">
          <div class="card-body">
            <h5 class="card-title text-warning">Pending Tasks</h5>
            <h3 class="text-warning">{{ pendingTasks }}</h3>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card border-danger">
          <div class="card-body">
            <h5 class="card-title text-danger">Failed Tasks</h5>
            <h3 class="text-danger">{{ failedTasks }}</h3>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "TaskCounters",
    props: ["completedTasks", "pendingTasks", "failedTasks"], // Recibe los contadores como props
  };
  </script>
  