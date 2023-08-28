<!-- A table for student progress -->
<!-- uses a ProgressRow component for each student  -->
<template>
  <div id="table-from-rows" class="fixed_header">
    <table>
      <thead>
        <tr>
          <th v-for="header in headers" :key="header">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <jupyter-widget v-for="child in children" :key="child" :widget="child"></jupyter-widget>
      </tbody>
    </table>
  </div>
</template>

<script>

export default {
  name: "ProgressTable",
  props: {
    headers: Array,
    select_key: String,
    selected: Object
  }
};
</script>

<style>

/* fixed headers from https://www.w3docs.com/snippets/html/how-to-create-a-table-with-a-fixed-header-and-scrollable-body.html */
/* use table id to scope the styles to this type of table */

#table-from-rows {
  position: relative;
}

#table-from-rows > table {
  width: 100%;
  min-width: fit-content;
  border-collapse: collapse;
}


.fixed_header {
  overflow-y: auto;
  width: 100%;
  height: 400px;
}


.fixed_header thead th {
  position: sticky;
  top: 0;
  background-color: #f2f2f2;
  color: black;
  z-index: 10;
}



#table-from-rows tr:hover {
  background-color: #d7d7d7;
}

#table-from-rows tbody > tr {
  border-bottom: 1px solid #d7d7d7;
}

#table-from-rows td, th {
  padding-block: 0.5em;
  text-align: center;
}

/* every other row */
#table-from-rows tbody > tr:nth-child(odd):not(:hover) {
  background-color: #fff2a944;
}
</style>
