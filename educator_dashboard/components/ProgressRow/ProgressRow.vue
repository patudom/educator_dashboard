<!-- progress row shows column_data name id and an externally defined progress bar -->
<template>
  <tr 
    class="progress-table-row"
    @click="() => selected = column_data"
    >
    
    <td v-for="key in Object.keys(column_data)" :key="key" :class="`progress-table-td progress-table-${key}`">
      {{ column_data[key] }}
    </td>

    <td
      class="progress-table-td progress-table-progress-bar"
      >
      <jupyter-widget :widget="progress_bar"></jupyter-widget>
    </td>
    
  </tr>
</template>

<script>

export default {
  name: "ProgressRow",

  props: {
    column_data: {
      type: Object,
      required: true
    },
    progress_bar: {
      type: Array,
      required: true
    },  
    style: {
      type: Object,
      default: () => ({height: "4px"})
    },
    selected: {
      type: Object,
      required: true
    }
  },

  mounted() {
    console.log("ProgressRow mounted");
  },

  methods: {
    
  }
};
</script>

<style>
/* left align cells */
/* add borders */
.progress-table-td {
  vertical-align: middle;
  padding-left: 5px;
  padding-right: 5px;
}
</style>
