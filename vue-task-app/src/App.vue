<template>
  <div class="container my-4">
    <HeaderComponent :createTask="createTask" />
    <TaskCounters
      :completedTasks="counts.completed"
      :pendingTasks="counts.pending"
      :failedTasks="counts.failed"
    />
    <TaskList :tasks="tasks" />
    <PaginationControls
      :currentPage="currentPage"
      :totalPages="totalPages"
      @page-change="fetchTasks"
    />
  </div>
</template>

<script>
import { getTasks, getTaskCount,createTask } from "@/services/api";
import HeaderComponent from "./components/HeaderComponent.vue";
import TaskCounters from "./components/TaskCounters.vue";
import TaskList from "./components/TaskList.vue";
import PaginationControls from "./components/PaginationControls.vue";

export default {
  name: "App",
  components: {
    HeaderComponent,
    TaskCounters,
    TaskList,
    PaginationControls,
  },
  data() {
    return {
      tasks: [], // Task list
      currentPage: 1, // Current page number
      pageSize: 10, // Number of tasks per page
      totalPages: 1,      // Total pages
      totalTasks: 0,      // Total number of tasks
      counts: {
        pending: 0,
        completed: 0,
        failed: 0,
      },
      websocket: null, // WebSocket instance for updates
    };
  },
  computed: {
    completedTasksCount() {
      return this.tasks.filter((task) => task.status === "completed").length;
    },
    pendingTasksCount() {
      return this.tasks.filter((task) => task.status === "pending").length;
    },
    failedTasksCount() {
      return this.tasks.filter((task) => task.status === "failed").length;
    },
  },
  methods: {
    async createTask() {
      await createTask();
      this.fetchTasks(this.currentPage);
    },
    async fetchCounts() {
    const pendingCount = await getTaskCount("pending");
    const completedCount = await getTaskCount("completed");
    const failedCount = await getTaskCount("failed");

    this.counts.pending = pendingCount.data.count;
    this.counts.completed = completedCount.data.count;
    this.counts.failed = failedCount.data.count;

  },
    async fetchTasks(page) {
      // Ensure page doesn't go below 1 or above totalPages
      // (assuming you know totalPages, otherwise just limit when incrementing/decrementing)
      if (page < 1) page = 1;
      if (page > this.totalPages) page = this.totalPages;

      const offset = (page - 1) * this.pageSize;
      const response = await getTasks(this.pageSize, offset);

      this.tasks = Object.entries(response.data.items).map(([task_id, data]) => ({
        task_id,
        ...data,
      }));

      // Update pagination info
      this.totalTasks = response.data.total_count;
      this.totalPages = Math.ceil(this.totalTasks / this.pageSize);
      this.currentPage = page; // Update currentPage to reflect the new page
    },
    setupWebSocket() {
      this.websocket = new WebSocket("ws://127.0.0.1:8000/ws");
      this.websocket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log("Message received from WebSocket:", data);
        
        // Example: Update task list dynamically if data includes new tasks
        if (data.type === "task_update") {
          console.log("Updating task list...");
          this.fetchTasks(this.currentPage);
          this.fetchCounts();
        }
      };
      this.websocket.onclose = () => {
        console.warn("WebSocket closed. Reconnecting...");
        setTimeout(this.setupWebSocket, 1000); // Reconnect on close
      };
    },
  },
  mounted() {
    this.fetchTasks(this.currentPage);
    this.fetchCounts();
    this.setupWebSocket();
  },
  beforeUnmount() {
    if (this.websocket) {
      this.websocket.close();
    }
  },
};
</script>

<style>
body {
  background-color: #f8f9fa;
}
.text-truncate {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

</style>