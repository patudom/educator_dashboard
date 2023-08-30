<template>
  
  <v-data-table
    class='dashboard-table'
    :headers="headers"
    :items="items"
    :itemKey="itemKey"
    :singleSelect="true"
    :disable-pagination="disable_pagination"
    @click:row="rowClick"
    hide-default-footer
    dense
  />

</template>


<script>
export default {
  name: 'DataTableHighlight',


  props: {
    headers: {
      type: Array,
      required: true
    },
    items: {
      type: Array,
      required: true
    },

    itemKey: {
      type: String,
      required: true
    },

    singleSelect: {
      type: Boolean,
      default: true
    },

    disable_pagination: {
      type: Boolean,
      default: true
    },

    on_click: {
      type: Function,
      required: true
    },

    highlight: {
      type: Boolean,
      default: true
    },

    deselect: {
      type: Boolean,
      default: true
    }
    
  },

  data() {
    return {
      selected: null
    }
  },


  methods: {
    rowClick(item, row, event) {
      console.log('rowClick', item, row)

      row.select(this.highlight & this.deselect & !(this.selected === item))

      this.selected = this.selected === item ? null : item
      
      this.on_click(this.selected)
      
      
    }
  }
}


</script>

<style>
  tr.v-data-table__selected {
    background: #d7d7d7 !important;
  }
  
  .dashboard-table tr th:first-of-type {
    width: 3ch;
  }
  
  .dashboard-table tr td:first-of-type {
    width: 3ch;
  }
  
</style>