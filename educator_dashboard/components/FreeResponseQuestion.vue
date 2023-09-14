<template>
    <div class="free-response-question">
        <div v-if="!hideShortQuestion" class="short-question">
          {{ shortquestion }}
        </div>

        <div v-if="!hideQuestion" class="question">
          {{ question }}
        </div>

        <div  v-if="!hideResponses" class="response-row" v-for="(response, index) in responseList">
          <div class="name-item" v-if="names != null && !hideName" >
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
    },

    hideShortQuestion: {
      type: Boolean,
      default: false
    },

    hideQuestion: {
      type: Boolean,
      default: false
    },

    hideResponses: {
      type: Boolean,
      default: false
    },

    hideName: {
      type: Boolean,
      default: false
    },
    
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
  /* grid-template-columns: auto auto;
  grid-template-rows: auto; */
  /* grid-gap: 10px; */

  padding: 0.5rem 0rem;
  margin-left: 1rem;
}

.free-response-question div {
  /* padding: 0.25rem; */
}
.short-question {
  display: inline-block;
  
}
.question {
  display: inline-block;
  color: black;
}

.response-row {

  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: auto;
  gap: 0.1rem;
  margin-top: 0.5rem;
}

.response-item {
  display: inline-block;
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  color: var(--md-grey-900);
  background-color: var(--md-amber-100);

}

.name-item {
  display: inline-block;
  font-weight: bold;
  color: var(--md-grey-900);
  padding-left: 0.5rem;
  margin-top: 1rem;

}
</style>
