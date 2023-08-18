<template>

  <div 
    class="jprogress-bar-container"
    :style="{...cssProps}"
    >
      <div 
        class="jprogress-bar-progress" 
        :style="{width: `${progress}%`, height: `${height}`, ...cssProps}">
      </div>
  </div>

  
</template>



<script>
export default {
  name: 'JProgressBar',

  props: {
    progress: {
      type: Number,
      default: 0
    },

    color: {
      type: String,
      default: '#4CAF50'
    },

    backgroundColor: {
      type: String,
      default: '#f1f1f1'
    },

    unfilledColor: {
      type: String,
      default: null
    },

    height: {
      type: String,
      default: '20px'
    }
  },

  computed: {
    cssProps() {
      return {
        '--backgroundColor': this.backgroundColor ,
        '--color': this.color,
        '--unfilledColor': this.unfilledColor || this.backgroundColor
      }
    }
  }
  
}
</script>

<style scoped>
.jprogress-bar-container {
  display: inline-block;
  position: relative;
  background-color: blue;
  border-radius: 5px;
  height: fit-content;
  margin: 5px;
  border: 1px solid black;
  
}

.jprogress-bar-progress {
  background-color: red;
  min-width: 5px;
}

</style>