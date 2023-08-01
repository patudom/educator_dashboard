<!-- A table for student progress -->
<!-- uses a ProgressRow component for each student  -->
<template>
  <div id="table-from-rows">
    <table>
      <thead>
        <tr>
          <th v-for="header in headers" :key="header">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <jupyter-widget v-for="row in rows" :key="row" :widget="row"></jupyter-widget>
      </tbody>
    </table>
  </div>
</template>

<script>

export default {
  name: "ProgressTable",
  props: {
    headers: Array,
    rows: Array,
  }
};
</script>

<style>

#table-from-rows > table {
  margin: 10px;
}

#table-from-rows > table tr td:last-child {
  width: 100%;
}
</style>
