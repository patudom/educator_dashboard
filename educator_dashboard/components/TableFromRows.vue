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
  margin-top: 0.75rem;
}

#table-from-rows > table {
  width: 100%;
  min-width: fit-content;
  border-collapse: collapse;
}


.fixed_header_table_wrapper {
  overflow-y: auto;
  width: 100%;
  max-height: var(--table-height);
}


.fixed_header_table_wrapper > table > thead {
  position: sticky;
  top: 0;
  background-color: var(--md-blue-800);
  color: white;
  z-index: 2;
}

.fixed_header_table_wrapper > table > tbody > tr > td:nth-child(3),
.fixed_header_table_wrapper > table > thead > tr > th:nth-child(3) {
  position: sticky;
  left: 0;
  z-index: 1;
}


.fixed_header_table_wrapper > table > tbody > tr:not(:hover) > td:nth-child(3) {
  background-color: inherit;
}

.fixed_header_table_wrapper > table > tbody > tr:hover > td:nth-child(3) {
  background-color: inherit;
}

.fixed_header_table_wrapper > table > thead > tr > th:nth-child(3)  {
  background-color: var(--md-blue-800);
}

#table-from-rows tbody tr {
  background-color: white;
}

#table-from-rows > table > tbody tr:hover {
  background-color: var(--md-grey-300);

}



#table-from-rows thead>tr:hover {
  background-color: unset;
}

#table-from-rows td, th {
  padding-block: 0.5em;
  text-align: center;
}

</style>
