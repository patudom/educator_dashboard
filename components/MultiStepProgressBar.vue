<script setup>
import { ref } from 'vue'

const msg = ref('Hello World!')
</script>

<template>
  <div class="progress-container">
    <div class="multi-progress-bar" :style="cssProps">
      
      <div v-for="step in steps" 
          :key="step" 
          class="step-wrapper"
          >
          <div 
            :class="[getStepClass(step), 'meter']"
            :style="{ width: getStepProgress(step), height: `${height}` }"
            ></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MultiStepProgressBar',
  props: {
    steps: {
      type: Number,
      default: 7
    },
    currentStep: {
      type: Number,
      default: 6
    },
    currentStepProgress: {
      type: Number,
      default: 50,
    },
    height: {
      type: Number,
      default: "20px"
      }
  },

  mounted() {
    console.log("MultiStepProgressBar mounted");
    console.log(`steps: ${this.steps} currentStep: ${this.currentStep} currentStepProgress: ${this.currentStepProgress}`)
  },

  methods: {
    getStepClass(step) {
      if (step < this.currentStep) {
        return 'completed';
      } else if (step === this.currentStep) {
        if (this.currentStepProgress === 100) {
          return 'completed';
        } else {
          return 'in-progress';
        }
      } else {
        return 'not-started';
      }
    },

    getStepProgress(step) {
      if (step < this.currentStep) {
        return '100%';
      } else if (step === this.currentStep) {
        return this.currentStepProgress + '%';
      } else {
        return '50%';
      }
    }
  },

  computed: {
    cssProps() {
      return { 
        '--number-steps': this.steps,
        '--meter-height': this.height
        }

    }
  }
}
</script>

<style>

.progress-container {
}

.multi-progress-bar {
  display: grid;
  grid-template-columns: repeat(var(--number-steps), 1fr) ;
  min-width: 200px;
  /* outline: 1px solid grey; */
  gap: 0px;
  padding: 2px;
  height: fit-content;
}

.step-wrapper {
  position: relative;
  outline: .5px solid white;
  padding-inline: 0;
  padding-block: 0;
  background-color: #fffa;
}

.meter {
  margin-left: 0;
  margin-right: auto;
  margin-block: auto;
  min-width: 5px;
}


.completed {
  background-color: #4CAF50;
}

.in-progress {
  background-color: #2196F3;
}

.not-started {
  background-color: #ca3030;
}


</style>
