<template>
  <div>

    <v-btn
      v-if="manualRefresh"
      :color="manualRefreshColor"
      @click="onClick"
    >
      <v-icon>mdi-refresh</v-icon> Manual Refresh
    </v-btn>

    
    <v-btn
      v-if="stopStart"
      :color="paused ? startColor : stopColor"
      @click="paused ? startRefresh() : reset()"
    >
      <v-icon>{{ paused ? 'mdi-refresh' : 'mdi-pause' }}</v-icon>
      {{ paused ? 'Resume' : 'Pause' }}
      
    </v-btn> 

    

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

    manualRefresh: {
      type: Boolean,
      required: false,
      default: false
    },

    stopStart: {
      type: Boolean,
      required: false,
      default: false
    },
    manualRefreshColor: {
      type: String,
      required: false,
      default: 'primary'
    },
    startColor: {
      type: String,
      required: false,
      default: '#8FBC8F'
    },

    stopColor: {
      type: String,
      required: false,
      default: '#B22222'
    }
    
  },

  data() {
    return {
      intervalId: null,
      loopCount: 0,
      paused: false,
    }
  },

  methods: {
    reset() {
      clearInterval(this.intervalId);
      this.paused = true;
    },


    startRefresh() {
      console.log('starting refresh')
      this.paused = false;
      this.intervalId = setInterval(() => {
        this.on_refresh();
        this.loopCount++;
        if (this.maxRepeat > 0 && this.loopCount >= this.maxRepeat) {
          clearInterval(this.intervalId);
        }
      }, this.periodInMilliseconds);
    },

    onClick() {
      this.on_refresh();
    }
  },

  mounted() {
    this.startRefresh();
  },

  beforeDestroy() {
    console.log('beforeDestroy')
    this.reset();
  },

  watch: {
    intervalId() {
      console.log('intervalId changed', this.intervalId)
    },

    loopCount() {
      console.log('looping')
    },
    
    paused(val) {
      if (val) {
        clearInterval(this.intervalId);
      }
    }
  }
}
</script>
