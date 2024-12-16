<template>
  <div class="table-responsive">
    <table class="table table-bordered table-hover align-middle">
      <thead class="custom-table-header">
        <tr>
          <th scope="col">Task ID</th>
          <th scope="col" class="text-center">Status</th>
          <th scope="col" class="text-center">Start Date</th>
          <th scope="col" class="text-center">End Date</th>
          <th scope="col" class="text-center">Duration (Seconds)</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="task in tasks"
          :key="task.task_id"
          :class="{
            'table-success': task.status === 'completed',
            'table-warning': task.status === 'pending',
            'table-danger': task.status === 'failed',
          }"
        >
          <!-- Task ID -->
          <td class="text-truncate" style="max-width: 60%;">{{ task.task_id }}</td>

          <!-- Status Badge -->
          <td class="text-center">
            <span
              :class="{
                'badge bg-success': task.status === 'completed',
                'badge bg-warning text-dark': task.status === 'pending',
                'badge bg-danger': task.status === 'failed',
              }"
              style="font-size: 0.85rem; padding: 0.4rem 0.6rem;"
            >
              {{ capitalize(task.status) }}
            </span>
          </td>

          <!-- Start Date -->
          <td class="text-center">
            <span :title="task.start_date">{{ formatDate(task.start_date) }}</span>
          </td>

          <!-- End Date -->
          <td class="text-center">
            <span :title="task.end_date">{{ formatDate(task.end_date) }}</span>
          </td>

          <!-- Duration in Seconds -->
          <td class="text-center">
            {{ calculateDuration(task.start_date, task.end_date) }} seconds
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "TaskList",
  props: ["tasks"], // Receives the task list as a prop
  methods: {
    capitalize(value) {
      return value.charAt(0).toUpperCase() + value.slice(1);
    },
    formatDate(dateStr) {
      if (!dateStr) return "N/A";
      const date = new Date(dateStr);
      return new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      }).format(date);
    },
    calculateDuration(startDate, endDate) {
      if (!startDate || !endDate) return "N/A";
      const start = new Date(startDate);
      const end = new Date(endDate);
      const duration = Math.round((end - start) / 1000); // Duration in seconds
      return duration >= 0 ? duration : "Invalid";
    },
  },
};
</script>

<style scoped>
.custom-table-header th {
  background-color: #f0f8ff !important; /* Soft blue */
  color: #003366 !important; /* Dark blue text */
  font-size: 1rem;
  font-weight: 600;
  text-align: center;
  border-bottom: 2px solid #dee2e6;
  padding: 12px;
}

.text-truncate {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.table-hover tbody tr:hover {
  background-color: #f9f9f9;
}

.table-success {
  background-color: #e7f5e7 !important;
}

.table-danger {
  background-color: #fbe8e8 !important;
}

.table-warning {
  background-color: #fdf2d6 !important;
}

.text-center {
  text-align: center;
}
</style>
