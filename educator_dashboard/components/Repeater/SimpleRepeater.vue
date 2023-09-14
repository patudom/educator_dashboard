<template>
  <div :class="['simple-repeater', showDebug ? '' : 'hidden']">
    <div v-if="showDebug">
      <p> pause: {{ pause }}</p>
      <p> reset: {{ reset }}</p>
      <p> done: {{ done }}</p>
      <p> loopCount: {{ loopCount }}</p>
      <p> intervalId: {{ intervalId }}</p>
      <p> maxRepeat: {{ maxRepeat }}</p>
      <p> period (ms): {{ periodInMilliseconds }}</p>
    </div>
  </div>

</template>

<script>
export default {
  name: 'Repeater',
  props: {
    periodInMilliseconds: {
      type: Number,
      required: true
    },
    maxRepeat: {
      type: Number,
      required: false,
      default: 0
    },
    on_refresh: {
      type: Function,
      required: true,
      default: () => {console.log('js on_refresh')}
    },
    reset: {
      type: Boolean,
      required: false,
      default: false
    },

    pause: {
      type: Boolean,
      required: false,
      default: false
    },
    
    showDebug: {
      type: Boolean,
      required: false,
      default: false
    },

    ping: {
      type: Number,
      required: false,
      default: 0
    }
    
    
  },

  data() {
    return {
      intervalId: null,
      loopCount: 0,
      done: false
    }
  },

  methods: {

    startRefresh() {
      if (this.pause) {
        return;
      }
      this.intervalId = setInterval(() => {
        this.on_refresh();
        this.loopCount++;
        if (this.maxRepeat > 0 && this.loopCount >= this.maxRepeat) {
          clearInterval(this.intervalId);
          this.done = true;
        }
      }, this.periodInMilliseconds);
    },
  },

  mounted() {
    // write a console log showing period and starting loop and if it is paused and when it will stop
    // console.log(`simple-repeat:mounted: period=${this.periodInMilliseconds}ms, maxRepeat=${this.maxRepeat}, pause=${this.pause}`)
    console.log('simple-repeat:  mounted')
    console.log(`simple-repeat:  period ${this.periodInMilliseconds}ms (${this.periodInMilliseconds / 1000}s)`)
    console.log(`simple-repeat:  maxRepeat ${this.maxRepeat} [0=forever]`)
    console.log(`simple-repeat:  Loop is now ${this.pause ? 'paused' : 'running'}`)
    this.startRefresh();
  },

  beforeDestroy() {
    console.log('clearing interval before destroy')
    clearInterval(this.intervalId);
  },

  watch: {
    intervalId() {
      console.log('intervalId changed', this.intervalId)
    },

    loopCount() {
      console.log('simple-repeat:looping')
    },

    reset(val) {
      console.log('simple-repeat:resetting', val)
      if (val) {
        clearInterval(this.intervalId)
        this.loopCount = 0;
        this.startRefresh();
        this.$emit('simple-repeat:reset', false);
      }
    },

    pause(val) {
      if (val) {
        console.log(`pausing at loopCount=${this.loopCount}`)
        clearInterval(this.intervalId);
        this.$emit('simple-repeat:pause');
      } else {
        console.log(`unpausing at loopCount=${this.loopCount}`)
        clearInterval(this.intervalId);
        this.startRefresh();
        this.$emit('simple-repeat:unpause');
      }
    },

    done() {
      if (this.done) {
        console.log('simple-repeat:done')
        this.$emit('simple-repeat:done');
      }
    },

    ping() {
      console.log('simple-repeat:manual-refresh')
      this.on_refresh();
      this.$emit('simple-repeat:manual-refresh');
    }
  }
}
</script>

<style>

.hidden {
  display: none;
}

</style>
