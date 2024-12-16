<template>
  <div class="row text-center mb-4">
    <div class="col-md-4">
      <div class="card border-success">
        <div class="card-body">
          <h5 class="card-title text-success">Completed Tasks</h5>
          <h3
            class="text-success animated-count"
            :class="{ 'animate': animated.completed }"
            @animationend="resetAnimation('completed')"
          >
            {{ completedTasks }}
          </h3>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card border-warning">
        <div class="card-body">
          <h5 class="card-title text-warning">Pending Tasks</h5>
          <h3
            class="text-warning animated-count"
            :class="{ 'animate': animated.pending }"
            @animationend="resetAnimation('pending')"
          >
            {{ pendingTasks }}
          </h3>
        </div>
      </div>
    </div>
    <div class="col-md-4">
      <div class="card border-danger">
        <div class="card-body">
          <h5 class="card-title text-danger">Failed Tasks</h5>
          <h3
            class="text-danger animated-count"
            :class="{ 'animate': animated.failed }"
            @animationend="resetAnimation('failed')"
          >
            {{ failedTasks }}
          </h3>
        </div>
      </div>
    </div>
  </div>
</template>

  
  <script>
  export default {
    name: "TaskCounters",
    props: ["completedTasks", "pendingTasks", "failedTasks"],
    data() {
      return {
        animated: {
          completed: false,
          pending: false,
          failed: false,
        },
      };
    },
    watch: {
      completedTasks() {
        console.log("completedTasks changed");
        this.animateCounter("completed");
      },
      pendingTasks() {
        this.animateCounter("pending");
      },
      failedTasks() {
        this.animateCounter("failed");
      },
    },
    methods: {
      animateCounter(type) {
        this.animated[type] = true;
      },
      resetAnimation(type) {
        this.animated[type] = false;
      },
    },
  };
  </script>

<style scoped>
.animated-count {
  display: inline-block;
  transition: transform 0.3s ease-in-out;
}

.animated-count.animate {
  animation: grow-shrink 0.3s ease-in-out;
}

@keyframes grow-shrink {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.5);
  }
  100% {
    transform: scale(1);
  }
}
</style>