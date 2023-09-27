<template>
  
  <v-data-table
    :class="['dashboard-table', ...classes]"
    :headers="headers"
    :items="items"
    :itemKey="itemKey"
    :singleSelect="true"
    :disable-pagination="disable_pagination"
    @click:row="rowClick"
    hide-default-footer
    hide-default-header
    dense
  >
  <!-- there header should be able to HTML code that gets rendered, so use a slot -->
    <template v-slot:header="{ props: {headers} }">
      <thead class="full-width-header-slot">
        <tr>
          <th v-for="header in headers" :key="header.text">
            <!-- if header has header.tooltip display tooltip -->
            <v-tooltip v-if="header.tooltip" bottom>
              <template v-slot:activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on" v-html="header.text"></span>
              </template>
              <span>{{ header.tooltip }}</span>
            </v-tooltip>
            <span v-else v-html="header.text"></span>
            
          </th>
        </tr>
      </thead>
    </template>
    
    <!-- this is the default slot for the table, so it will render the data -->
    <!-- <template v-slot:default="{ items, headers }">
      <tbody>
        <tr v-for="item in items" :key="item[itemKey]" :class="{'v-data-table__selected': selected === item}">
          <td v-for="header in headers" :key="header.text" :class="header.class">
            <span v-html="item[header.value]"></span>
          </td>
        </tr>
      </tbody>
    </template> -->
  </v-data-table>

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
    },
    
    // list of class names to apply to table
    classes: {
      type: Array,
      default: () => []
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
 
  @media screen and (max-width: 600px) {
    .full-width-header-slot {
      display: none;
    }
  }
  
</style>

