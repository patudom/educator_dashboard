<!-- A table for student progress -->
<!-- uses a ProgressRow component for each student  -->
<template>
  <div>
    <table>
      <thead>
        <tr>
          <th scope="col">Student ID</th>
          <th scope="col">Name</th>
          <th scope="col">Progress</th>
        </tr>
      </thead>
      <tbody>
        <ProgressRow v-for="student in students" :key="student.id" :student="student" />
      </tbody>
    </table>
  </div>
</template>

<script>
import ProgressRow from "@/components/ProgressRow.vue";
export default {
  name: "ProgressTable",
  components: {
    ProgressRow
  },
  props: {
    students: Array
  }
};
</script>

<style scoped>
table {
  width: 100%;
}
</style>
