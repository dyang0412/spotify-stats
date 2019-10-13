<template>
    <div class="stat-page">
        <app-search-bar 
            @gotTrack="Track = $event; init = true;"
            @gotTrackAnal="TrackAnal = $event"
            @gotTrackFeatures="TrackFeatures = $event"
            @gotAlbumImg="AlbumUrl = $event"
            @gotAlbum="Album = $event"
            @gotArtist="Artist = $event"
            ></app-search-bar>
        <br>
        <div v-if="init" id="tracksection" class="container row m-auto">
            <div class="col-md-6">
                <div class="panel col-md-12">
                    <div class="row m-auto pt-3 trackheader">
                        <div class="col-lg-12 col-md-12 col-sm-12">
                            <h2 ><ion-icon name="musical-notes"></ion-icon> Track: </h2>
                        </div>
                    </div>
                    <div class="row m-auto pt-3">
                        <div class="col-lg-12 col-md-12 col-sm-12">
                            <h4>{{ Track.name }} <span class="explicit" v-if="Track.explicit">EXPLICIT</span> </h4>
                            <h5 style="color: rgb(156, 156, 156);">
                                <ul id="artistlist" class="p-0">
                                    <li v-for="artist in Track.artists" :key="artist.name">{{ artist.name }}</li>
                                </ul>
                            </h5>
                        </div>
                    </div>
                    <div class="row m-auto pt-3">
                        <div class="col-md-7 col-sm-12 p-0" style="transform: translateY(-4rem)">
                            <div id="chart">
                                <apexchart type=radar height=350 :options="chartOptions" :series="getTrackFeatures" />
                            </div>
                        </div>
                        <div class="col-md-5 col-sm-12">
                            <div class="container p-0">
                                <table class="table table-borderless text-left">
                                    <tbody>
                                        <tr>
                                            <th scope="row">Popularity</th>
                                            <td>{{ Track.popularity }}</td>
                                        </tr>
                                        <tr>
                                            <th scope="row">Duration</th>
                                            <td>{{ getDuration }}</td>
                                        </tr>
                                        <tr>
                                            <th scope="row">Available Markets</th>
                                            <td>{{ Track.available_markets.length }}</td>
                                        </tr>
                                        <tr>
                                            <th scope="row">Key</th>
                                            <td>{{ getKey }}</td>
                                        </tr>
                                        <tr>
                                            <th scope="row">Mode</th>
                                            <td>{{ getMode }}</td>
                                        </tr>
                                        <tr>
                                            <th scope="row">Tempo</th>
                                            <td>{{ TrackAnal.track.tempo }}</td>
                                        </tr>
                                        <tr>
                                            <th scope="row">Time Signature</th>
                                            <td>{{ TrackAnal.track.time_signature }}/4</td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

           <div class="artist col-md-6 col-sm-12">
               <div class="panel col-md-12">
                   <div class="row m-auto pt-3 trackheader">
                        <div class="col-lg-12 col-md-12 col-sm-12">
                            <h2><ion-icon name="person"></ion-icon> Artist: </h2>
                        </div>
                    </div>
                    <div class="row m-auto pt-3">
                        <div class="col-lg-12 col-md-12 col-sm-12">
                            <h4>{{ Artist.name }}</h4>
                        </div>
                    </div>
                    <div class="row m-auto pt-3">
                        <div class="col-md-6 col-sm-12 p-0">
                            <div class="container">
                                <img class="img-fluid shadow " :src="Artist.images[1].url"> 
                            </div>
                        </div>
                        <div class="col-md-6 col-sm-12">
                            <div class="col-md-3 col-sm-12 p-0">
                                <div class="container p-0">
                                    <table class="table table-borderless text-left">
                                        <tbody>
                                            <tr>
                                                <th scope="row">Popularity</th>
                                                <td>{{ Artist.popularity }}</td>
                                            </tr>
                                            <tr>
                                                <th scope="row">Followers</th>
                                                <td>{{ Artist.followers.total }}</td>
                                            </tr>
                                            <tr>
                                                <th scope="row">Genres</th>
                                                <td>
                                                    <ul class="list-group">
                                                        <li v-for="genre in Artist.genres" :key="genre">{{ genre }}</li>
                                                    </ul>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
               </div>
            </div>
        </div>
        
        <div v-if="init" class="container row m-auto pt-4">
            <div class="col-md-12 col-sm-12">
                <h2 ><ion-icon name="disc"></ion-icon> Album: </h2>
            </div>
        </div>
        <div v-if="init" id="artist" class="container row m-auto pt-2">
            <div class="col-md-3 col-sm-12 p-0">
                <div class="container">
                    <h4>{{ Artist.name }}</h4>
                    <img class="img-fluid shadow " :src="AlbumUrl">
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import SearchBar from './SearchBar.vue'
import VueApexCharts from 'vue-apexcharts'
export default {
    data(){
        return{
            init: false,
            Track: {},
            Artist: {},
            Album: {},
            AlbumUrl: '',
            TrackAnal: {},
            TrackFeatures: {},
            chartOptions: {
                labels: ['Acousticness','Energy','Danceability','Instrumentalness','Liveness','Speechiness','Valence'],
                yaxis: {
                    show: false,
                    max: 1,
                    min: 0
                },
                tooltip:{
                    theme: 'dark'
                },
                chart:{
                    toolbar:{
                        show: false
                    }
                }
            }
            
        }
    },
    computed:{
        getTrackFeatures(){
            return [{
                name: 'Series 1',
                data: [
                        this.TrackFeatures.acousticness,
                        this.TrackFeatures.energy,
                        this.TrackFeatures.danceability,
                        this.TrackFeatures.instrumentalness,
                        this.TrackFeatures.liveness,
                        this.TrackFeatures.speechiness,
                        this.TrackFeatures.valence]
            }] 
        },
        getDuration(){
            var millis = this.Track.duration_ms;
            var minutes = Math.floor(millis / 60000);
            var seconds = ((millis % 60000) / 1000).toFixed(0);
            return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
        },
        getMode(){
            return (this.TrackAnal.track.mode > 0 ? 'Major' : 'Minor')
        },
        getKey(){
            switch(this.TrackAnal.track.key){
                case (0):
                    return 'C'
                case (1):
                    return 'C♯'
                case (2):
                    return 'D'
                case (3):
                    return 'D♯'
                case (4):
                    return 'E'
                case (5):
                    return 'F'
                case (6):
                    return 'F♯'
                case (7):
                    return 'G'
                case (8):
                    return 'G♯'
                case (9):
                    return 'A'
                case (10):
                    return 'A♯'
                case (11):
                    return 'B'
            }
        }
    },
    components:{
        appSearchBar: SearchBar,
        apexchart: VueApexCharts
    },
    mounted(){
        
    }
}
</script>

<style scoped>
    table{
        color:rgb(173, 173, 173)
    }

    h4{
        color: #fff;
    }

    h2{
        color: rgb(54, 199, 110);
    }

    ul{
        list-style: none
    }

    td, th{
        padding: 3px;
    }

    .trackheader{
        border-bottom: 1px solid rgb(71, 71, 71);
    }

    .panel{
        background-color: rgb(31, 31, 31);
        border-radius: 0.5rem;
        height: 100%;
    }


    #artistlist li{
        float: left;
    }

    #artistlist li::after{
        content: ', ';
        white-space: pre;
    }

    #artistlist li:last-child::after{
        content: ''
    }

    .artist img{
        border-radius: 50%;
    }

    .explicit{
        font-size: 10px;
        color: rgb(71, 71, 71);
        border: 1px solid rgb(71, 71, 71);
        padding: 4px;
        margin-left: 10px;
    }

    .stat-page{
        background-color: rgb(15, 15, 15);
        min-height: 100vh;
        min-width: 100%;
        padding-left: 300px;
    }

    #track{
        color: #fff;
    }

    #track img{
        height: 80%;
        width: 80%;
        border-radius: 50%;
    }

    #artist{
        color: #fff;

    }

    ion-icon{
        vertical-align:text-bottom;
        font-size: 35px;
    }

</style>