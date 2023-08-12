<script setup>
import Header from './components/AppHeader.vue'
import Footer from './components/AppFooter.vue'
</script>

<template>
  <div class="container py-4 px-3 mx-auto">
    <Header />

    <h2 v-if="!this.topic">Select the image topic you would like to see</h2>

    <div v-if="!this.topic" class="container marketing">

      <!-- START THE FEATURETTES -->

      <hr class="featurette-divider">

      <div class="row featurette">
        <div class="col-md-7">
          <h2 class="featurette-heading fw-normal lh-1">Animals</h2>
          <p class="lead">Enjoy a great collection of happy animals</p>
          <button type="button" class="btn btn-success me-3" v-on:click="selectTopic('Animals')">Select</button>
        </div>
        <div class="col-md-5">
          <img src="./assets/animals.png" />

        </div>
      </div>

      <hr class="featurette-divider">

      <div class="row featurette">
        <div class="col-md-7 order-md-2">
          <h2 class="featurette-heading fw-normal lh-1">High Views </h2>
          <p class="lead">See great views without climbing anywhere</p>
          <button type="button" class="btn btn-success me-3" v-on:click="selectTopic('High Views')">Select</button>
        </div>
        <div class="col-md-5 order-md-1">
          <img src="./assets/view.png" />
        </div>
      </div>

      <hr class="featurette-divider">

      <div class="row featurette">
        <div class="col-md-7">
          <h2 class="featurette-heading fw-normal lh-1">Sports</h2>
          <p class="lead">Watch neverseen pictures of venues</p>
          <button type="button" class="btn btn-success me-3" v-on:click="selectTopic('Sport venues')">Select</button>
        </div>
        <div class="col-md-5">
          <img src="./assets/sports_venues.png" />
        </div>
      </div>
      <hr class="featurette-divider">

      <!-- /END THE FEATURETTES -->

    </div>

    <div class="px-4 pt-5 my-5 text-center border-bottom" v-if="this.topic">
      <h1 class="display-4 fw-bold text-body-emphasis">{{ this.topic }}</h1>
      <div class="col-lg-6 mx-auto">
        <p class="lead mb-4" v-if="this.current_image_description">{{ this.current_image_description }}</p>

        <audio controls="controls" v-if="this.current_audio_b64" autobuffer="autobuffer" autoplay="autoplay">
          <source :src="'data:audio/wav;base64, ' + this.current_audio_b64" />
        </audio>
        <p class="lead mb-4" v-if="!this.current_image_description">{{ this.loading_step }}</p>
      </div>
      <div class="overflow-hidden">
        <div class="container px-5">
          <div v-if="!this.current_image_description" class="spinner-grow" style="width: 3rem; height: 3rem;"
            role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <img v-if="this.current_image_description" v-bind:src="'data:image/png;base64, ' + this.current_image_b64"
            class="img-fluid border rounded-3 shadow-lg mb-4" v-bind:alt="this.current_image_description" loading="lazy"
            width="700" height="700">
        </div>
      </div>
    </div>



    <Footer />
  </div>
</template>
<script>
export default {
  name: 'App',
  data: function () {
    return {
      topic: null,
      image_descriptions: [],
      current_image_description: '',
      current_image_b64: null,
      current_audio_b64: null,
      loading_step:""
    }
  },
  methods: {

    selectTopic: function (selected_topic) {
      console.log("Selecting topic " + selected_topic)
      this.topic = selected_topic
      this.getImageDescriptions()
    },

    getImageDescriptions: function () {
      this.loading_step = "Generating descriptions..."
      console.log("Sending request for topic " + this.topic)
      this.responseAvailable = false;
      fetch("https://ufsi1mrh26.execute-api.us-east-1.amazonaws.com/dev/description", {
        "method": "POST",
        "body": JSON.stringify({
          "message": this.topic
        })
      })
        .then(response => {
          if (response.ok) {
            return response.json()
          } else {
            console.log("Server returned " + response.status + " : " + response.statusText);
          }
        }).then(async response => {
          console.log(response)
          this.image_descriptions = response.descriptions;
          for (let i = 0; i < this.image_descriptions.length; i++) {
            
            this.getImage(this.image_descriptions[i])
            
            await sleep(10000)
          }
          setTimeout(() => {
            this.getImageDescriptions();
          }, "1000");
        })
        .catch(err => {
          console.log(err);
        });
    },

    getImage: function (description) {
      this.loading_step = "Generating image..."
      console.log("Sending request for description " + description)
      this.responseAvailable = false;
      fetch("https://ufsi1mrh26.execute-api.us-east-1.amazonaws.com/dev/image", {
        "method": "POST",
        "body": JSON.stringify({
          "message_id": description
        })
      })
        .then(response => {
          if (response.ok) {
            return response.json()
          } else {
            console.log("Server returned " + response.status + " : " + response.statusText);
          }
        })
        .then(response => {
          console.log("Loading image for " + description)
          this.current_image_b64 = response.image_b64;
          this.current_image_description = response.description
          this.getAudio(description)
        })
        .catch(err => {
          console.log(err);
        });
    },

    getAudio: function (description) {
      console.log("Sending request for description " + description)
      this.responseAvailable = false;
      fetch("https://ufsi1mrh26.execute-api.us-east-1.amazonaws.com/dev/audio", {
        "method": "POST",
        "body": JSON.stringify({
          "message_id": description
        })
      })
        .then(response => {
          if (response.ok) {
            return response.json()
          } else {
            console.log("Server returned " + response.status + " : " + response.statusText);
          }
        })
        .then(response => {
          console.log("Loading audio for " + description)
          this.current_audio_b64 = null
          return response.audio;
          
        })
        .then(audio_b64 => {
          this.current_audio_b64 = audio_b64
        })
        .catch(err => {
          console.log(err);
        });
    },
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

</script>