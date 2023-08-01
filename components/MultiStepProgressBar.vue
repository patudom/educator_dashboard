<script setup>
import { ref } from 'vue'

const msg = ref('Hello World!')
</script>

<template>
  <div class="progress-container">
    <div class="multi-progress-bar" :style="{gap: `${gap}`, ...cssProps}">
      
      <div v-for="step in steps" 
          :key="step" 
          :class="['step-wrapper', getStepClass(step)+'-lighter']"
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
    },
    gap: {
      type: Number,
      default: "0px"
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
        return '0%';
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
  /* outline: 3px solid grey; */
  padding: 2px;
  height: fit-content;
  /* background-color: white; */
}

.multi-progress-bar:hover {
  transform: scale(1.01);
}

.step-wrapper {
  position: relative;
  padding-inline: 0;
  padding-block: 0;
}

.meter {
  margin-left: 0;
  margin-right: auto;
  margin-block: auto;
  min-width: 5px;
}


.completed {
  background-color: rgb(76, 175, 80);
}

.completed-lighter {
  background-color: rgb(76, 175, 80,0.25);
}

.in-progress {
  background-color: rgb(33, 150, 243);
}

.in-progress-lighter {
  background-color: rgb(33, 150, 243,0.55);
}

.not-started {
  background-color: rgb(202, 48, 48);
}

.not-started-lighter {
  background-color: rgb(202, 48, 48,0.25);
}

</style>
