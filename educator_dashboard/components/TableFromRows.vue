<!-- A table for student progress -->
<!-- uses a ProgressRow component for each student  -->
<template>
  <div 
    id="table-from-rows" 
    :class="['fixed_header_table_wrapper', class_]"
    :style="cssProps"
    >
    <table>
      <thead>
        <tr>
          <th v-for="header in headers" :key="header" v-html="header"></th>
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
    selected: Object,
    table_height: String,
    class_: String,
  },

  computed: {
    cssProps() {
      return { 
        '--table-height': this.table_height,
        }

    }
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


.fixed_header_table_wrapper {
  overflow-y: auto;
  width: 100%;
  height: var(--table-height);
}


.fixed_header_table_wrapper > table > thead {
  position: sticky;
  top: 0;
  background-color: #f2f2f2;
  color: black;
  z-index: 2;
}



#table-from-rows tr:hover {
  background-color: #ededed;
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
