<!-- progress row shows column_data name id and an externally defined progress bar -->
<template>
  <tr 
    :class="`'progress-table-row' ${selected ? 'progress-table-row-selected' : ''}`"
    @click="() => selected = !selected"
    >
    
    <td v-for="key in Object.keys(column_data)" :key="key" :class="`progress-table-td progress-table-${key}`">
      {{ column_data[key] }}
    </td>
    
    <td 
      class="progress-table-td progress-table-progress"
      v-for="step in steps" 
      :key="step" 
      >
        <div
          :class="['step-wrapper', getStepClass(step)+'-lighter']"
          :style="{gap: `${gap}`, ...cssProps}"
          >
          <div 
            :class="[getStepClass(step), 'meter']"
            :style="{ width: getStepProgress(step) }"
            ></div>
  </div>

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

    style: {
      type: Object,
      default: () => ({height: "4px"})
    },
    selected: {
      type: Boolean,
      required: true
    },

    // progress bar props
    
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
    console.log("ProgressRow mounted");
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

.progress-table-row-selected {
  background-color: #d7d7d7;
}

.progress-table-progress {
  padding-left: 0;
  padding-right: 0;
  height: 1rem;
}

.step-wrapper {
  position: relative;
  padding-inline: 0;
  padding-block: 0;
  width: 15ch;
  height: inherit;
  border-radius: 999999px;  /* max out for rounded corners */
  overflow: hidden;
}

.meter {
  margin-left: 0;
  margin-right: auto;
  margin-block: auto;
  min-width: 5px;
  height: 100%;
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
