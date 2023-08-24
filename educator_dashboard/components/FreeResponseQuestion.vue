<template>
    <div class="free-response-question">
        <div class="short-question">
          {{ shortquestion }}
        </div>
        <div class="question">
          {{ question }}
        </div>
        <div class="response-row" v-for="(response, index) in responseList">
          <div class="name-item" v-if="names != null" >
            {{ getName(index) }}
          </div>
          <div class="response-item">
          {{ response }}
          </div>
        </div>
      </div>
</template>


<script>
export default {

  name: 'FreeResponseQuestion',

  props: {
    question: {
      type: String,
      default: ''
    },

    shortquestion: {
      type: String,
      default: ''
    },
    
    responses: {
      type: Array[String],
      default: ['']
    },

    names: {
      type: Array[String],
      default: null
    }
  },

  computed: {

    responseList() {
      // console.log(this.question, this.responses)
      // if responses is a string. put it in an array
      if (typeof this.responses === 'string') {
        return [this.responses]
      } else {
        return this.responses
      }
    }
  },

  methods: {
    getName(index) {

      if (this.names == null) {
        return null
      }

      if (Array.isArray(this.names) && this.names.length > index) {
          return this.names[index]
        } else if ((typeof this.names === 'string') || (typeof this.names === 'number')) {
          return this.names
        } else {
          return null
      }
      
    }
  }
}
</script>


<style scoped>
/* divs should be in columns on a grid.  */
/* if there are multiple responses they should be listed below each other */


.free-response-question {
  display: grid;
  grid-template-columns: auto auto;
  grid-template-rows: auto;
  grid-gap: 10px;
  background-color: rgba(2, 2, 2, 0.127);
}

.free-response-question div {
  padding: 0.25rem;
}
.short-question {
  display: inline-block;
  grid-row: 1;
  grid-column: 1;
  background-color: lightgreen;
  
}
.question {
  grid-column: 2;
  grid-row: 1;
  background-color: lightblue;
}

.response-row {
  grid-column: 1 / 3;
  background-color: rgb(227, 240, 128);
}

.response-item {
  display: inline-block;
  background-color: lightcoral;
}

.name-item {
  display: inline-block;
  background-color: lightpink;
}
</style>
