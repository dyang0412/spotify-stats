<template>
    <div id="searchcomponent">
        <div class="navbar fixed-top navbar-expand navbar-dark">
            <button @click="collapse" id="sidebarCollapse" class="btn btn-outline-success">
                <span class="navbar-toggler-icon"></span>
            </button>
        </div>   
        <div id="searchbar" class="search-bar fixed-top">
            <div id="header" class="row">
                <div class="col-md-12 text-center noselect">
                    <h3>Spotify Stats <StatsIcon id="StatsIcon" style="display: inline"></StatsIcon></h3>
                    <p>All data provided by Spotify</p>
                </div>
            </div>
            <transition name="slide" appear>
                <div id="input" class="row">
                    <div class="col-md-12 text-center">
                        <div class="form-group">
                            <div class="input-group pt-3 mb-3">
                                <label for="inp" class="inp">
                                    <input type="text" id="inp" placeholder="&nbsp;" @keyup.enter="onSubmit" v-model="query" required>
                                    <span class="label">Search for a track</span>
                                    <span class="border"></span>
                                </label>
                                <button @click="onSubmit" class="btn btn-outline-success w-75">Search</button>
                            </div>
                        </div>
                    </div>
                </div>
            </transition>
            <div id="search-results" class="row custom-scrollbar">
                <div class="col-md-12">
                    <div class="row pb-2 pt-2 border-bottom border-light trackResult" 
                        v-for="(track,index) in results" 
                        :key="index" 
                        @click="onSongSelect(track,track.id, track.artists[0].id, track.artists[0].name, track.album.id, track.album.images[1].url)">
                        <div class="col-lg-3 col-md-3 col-sm-3 col-3 pl-2">
                            <img :src="track.album.images[2].url">
                        </div>
                        <div class="col-lg-9 col-md-9 col-sm-9 col-9">
                            <p>{{track.name}}</p>
                            <p id="album">{{track.album.name}}</p>
                            <ul id="artistlist"><li v-for="(artist, i) in track.artists" :key="i" class="artist">{{artist.name}}</li></ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import StatsIcon from 'vue-ionicons/dist/md-stats.vue'
import Search from 'vue-ionicons/dist/md-search'
export default {
    data() {
        return {
            token: 'no token',
            query: '',
            results: []
        }
    },
    components:{
      StatsIcon : StatsIcon,
      Search
    },
    methods: {
        getToken() {
            //const path = 'http://localhost:5000/auth';
            const path = '//spotstats.cosinic.com/auth';
            axios.get(path)
                .then((res) => {
                    this.token = res.data.access_token;
                    //console.log('Access Token: ' + this.token)
                })
                .catch((error) => {
                // eslint-disable-next-line
                console.error(error);
            });
        },
        search(payload) {
            //const path = 'http://localhost:5000/search';
            const path = '//spotstats.cosinic.com/search';
            axios.post(path, payload)
                .then((res) => {
                    //console.log('Query Sent: ' + this.query)
                    //console.log(res.data)
                    this.results = res.data.tracks.items;
                })
                .catch((error) => {
                // eslint-disable-next-line
                console.log(error);
            });
        },
        onSubmit(evt) {
            evt.preventDefault();
            const payload = {
                trackname: this.query,
                token: this.token
            };
            this.search(payload);
            var list = this.$el.querySelector('#search-results');
            list.scrollTop = 0;
        },

        onSongSelect(track, trackid, artistid, artistname, albumid, albumurl){
            var width = (window.innerWidth > 0) ? window.innerWidth : screen.width;
            if(width <= 1310){
                this.collapse();
            }

            // Get Track Info
            this.$emit('gotTrackID', trackid)
            this.$emit('gotTrack', track)
            this.$emit('gotAlbumImg', albumurl)
            this.$emit('gotAlbumID', albumid)
            //console.log('Track ID: ' + trackid);
            //const trackpath1 = 'http://localhost:5000/get-trackAnal';
            const trackpath1 = '//spotstats.cosinic.com/get-trackAnal';
            //console.log('Looking up track...')
            const trackpayload1 = { trackID: trackid, token: this.token}
            axios.post(trackpath1, trackpayload1)
                .then((res) => {
                    this.$emit('gotTrackAnal', res.data)
                    //console.log(res.data)
                })
                .catch((error) => {
                console.log(error);
            });
            //const trackpath2 = 'http://localhost:5000/get-trackFeatures';
            const trackpath2 = '//spotstats.cosinic.com/get-trackFeatures';
            //console.log('Looking up track features...')
            const trackpayload2 = { trackID: trackid, token: this.token}
            axios.post(trackpath2, trackpayload2)
                .then((res) => {
                    this.$emit('gotTrackFeatures', res.data)
                    //console.log(res.data)
                })
                .catch((error) => {
                console.log(error);
            });

            //Get Artist Info
            //const artistpath = 'http://localhost:5000/get-artist';
            const artistpath = '//spotstats.cosinic.com/get-artist';
            //console.log('Looking up artist...')
            const artistpayload = { artistID: artistid, token: this.token}
            axios.post(artistpath, artistpayload)
                .then((res) => {
                    this.$emit('gotArtist', res.data)
                    //console.log(res.data)
                })
                .catch((error) => {
                console.log(error);
            });

            //const toptrackspath = 'http://localhost:5000/get-artistTopTracks';
            const toptrackspath = '//spotstats.cosinic.com/get-artistTopTracks';
            //console.log('Looking up artist...')
            const toptrackspayload = { artistID: artistid, token: this.token}
            axios.post(toptrackspath, toptrackspayload)
                .then((res) => {
                    this.$emit('gotTopTracks', res.data)
                    //console.log(res.data)
                })
                .catch((error) => {
                console.log(error);
            });

            //Get Album Info
            //const albumpath = 'http://localhost:5000/get-album';
            const albumpath = '//spotstats.cosinic.com/get-album';
            //console.log('Looking up album...')
            const albumpayload = { albumID: albumid, token: this.token}
            axios.post(albumpath, albumpayload)
                .then((res) => {
                    this.$emit('gotAlbum',res.data)
                    //console.log(res.data)
                })
                .catch((error) => {
                console.log(error);
            });

            this.$emit('createChart');
        },
        collapse(){
            $('#searchbar').toggleClass('active');
            this.$emit('collapse');
        }
    },
        
    created(){
        this.getToken();   
    }
}


</script>

<style scoped>
    *:focus {
        outline: none;
    }

    p{
        color: #fff;
        margin: 0;
        font-size: 15px;
    }

    #artistlist{
        list-style: none;
        padding: 0;
    }

    .artist{
        font-size: 12px;
        float: left;
        color: #fff;
    }

    .artist::after{
        content: ', ';
        white-space: pre;
    }

    .artist:last-child::after{
        content: ''
    }

    #album{
        font-size: 12px;
        color: rgb(156, 156, 156);
    }

    .navbar { 
        padding: 0;
        background-color:rgba(0, 0, 0);
        z-index: 2;
    }

    #sidebarCollapse { 
        margin: 4px;
    }

    .search-bar{
        position: fixed;
        top: 0;
        left: 0;
        padding-top: 0;
        width:300px;
        background-color: rgb(36, 36, 36);
        overflow: hidden;
        overflow-x: hidden;
        margin-top: 40px;
        height: 100%;
        z-index: 1;
        transition: all 0.3s;
    }

    .active{
        margin-left: -300px;
    }
    
    .row{
        width: 100%;
        margin: 0;
    }

    #header{
        background-color: rgb(54, 199, 110);
        padding-top: 10px;
    }


    #header p{
        font-size: 12px;
        margin: 0;
        padding-bottom: 5px;
        color: #fff;
    }

    button{
        color: rgb(54, 199, 110);
        border-color: rgb(54, 199, 110);
        margin: auto;
        margin-top: 10px;
    }

    #search-results{
        height: calc(77vh - 40px);
        overflow-y: scroll;
    }

    #search-results .col-md-12{
        height: 100%;
    }

    .trackResult{
        cursor: pointer;
    }

    .trackResult:hover{
        background-color: rgb(51, 51, 51);
        filter: alpha(opacity=100)
    }

    .border-light{
        border-color: rgb(83, 83, 83)!important;
    }

    .custom-scrollbar::-webkit-scrollbar {
        width: 8px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
        background : rgb(36, 36, 36);
        border-radius: 10px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background : rgba(77, 77, 77, 0.5);
        border-radius: 10px;
        box-shadow:  0 0 6px rgba(0, 0, 0, 0.5);
    }

    #StatsIcon{
        font-size: 30px;
        vertical-align:top
    }

    .noselect {
        -webkit-touch-callout: none; /* iOS Safari */
            -webkit-user-select: none; /* Safari */
            -khtml-user-select: none; /* Konqueror HTML */
            -moz-user-select: none; /* Old versions of Firefox */
                -ms-user-select: none; /* Internet Explorer/Edge */
                    user-select: none; /* Non-prefixed version, currently
                                        supported by Chrome, Opera and Firefox */
    }

    html,

    body {
        height: 100%;
    }
    body {
        display: grid;
        -webkit-text-size-adjust: 100%;
        -webkit-font-smoothing: antialiased;
    }
    * {
        box-sizing: border-box;
    }
    .inp {
        position: relative;
        margin: auto;
        width: 100%;
        max-width: 280px;
    }
    .inp .label {
        position: absolute;
        top: 16px;
        left: 0;
        font-size: 16px;
        color: #9098a9;
        font-weight: 500;
        transform-origin: 0 0;
        transition: all 0.2s ease;
        cursor: text;
    }
    .inp .border {
        position: absolute;
        bottom: 0;
        left: 0;
        height: 2px;
        width: 100%;
        background: rgb(54, 199, 110);
        transform: scaleX(0);
        transform-origin: 0 0;
        transition: all 0.15s ease;
    }
    .inp input {
        -webkit-appearance: none;
        width: 100%;
        border: 0;
        font-family: inherit;
        padding: 12px 0;
        height: 48px;
        font-size: 16px;
        font-weight: 500;
        border-bottom: 2px solid #c8ccd4;
        background: none;
        border-radius: 0;
        color: #fff;
        transition: all 0.15s ease;
    }
    .inp input:hover {
        background: rgba(34,50,84,0.03);
    }
    .inp input:not(:placeholder-shown) + span {
        color: rgb(54, 199, 110);
        transform: translateY(-26px) scale(0.75);
    }
    .inp input:focus {
        background: none;
        outline: none;
    }
    .inp input:focus + span {
        color: rgb(54, 199, 110);;
        transform: translateY(-26px) scale(0.75);
    }
        .inp input:focus + span + .border {
        transform: scaleX(1);
    }

    ::-webkit-input-placeholder { /* WebKit browsers */
        color: transparent;
    }
    :-moz-placeholder { /* Mozilla Firefox 4 to 18 */
        color:    transparent;
        opacity:  1;
    }
    ::-moz-placeholder { /* Mozilla Firefox 19+ */
        color:    transparent;
        opacity:  1;
    }
    :-ms-input-placeholder { /* Internet Explorer 10+ */
        color:    transparent;
    }

.slide-enter {
    opacity: 0;
}

.slide-enter-active {
    animation: slide-in 1s ease-out forwards;
    transition: opacity 0.75s;
}

.fade-enter {
    opacity: 0; 
}

.fade-enter-active {
    transition: opacity 1s;
}

@keyframes slide-in{
    from{
        transform:  translateY(50px);
    }
    to{
        transform: translateY(0);
    }
}

    /*---Media Queries---*/
@media (max-width: 992px) {
   
}

@media (max-width: 768px) {
    
}

@media (max-width: 576px) {

    
}
            
</style>
