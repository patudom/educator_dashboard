<!-- progress row shows student name id and multistepprogressbar -->
<template>
  <tr 
    class="progress-table-row"
    @click="() => selected = student"
    >
    
    <td v-for="key in Object.keys(student)" :key="key" :class="`progress-table-td progress-table-${key}`">
      {{ student[key] }}
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
    student: {
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
