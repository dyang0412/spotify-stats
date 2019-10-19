<template>
    <div class="stat-page">
        <app-search-bar 
            @gotTrack="Track = $event; init = true;"
            @gotTrackID="src = 'https://open.spotify.com/embed/track/' + $event"
            @gotAlbumID="playlist_src = 'https://open.spotify.com/embed/album/' + $event"
            @gotTrackAnal="TrackAnal = $event; getLoudness();"
            @gotTrackFeatures="TrackFeatures = $event"
            @gotAlbumImg="AlbumUrl = $event"
            @gotAlbum="Album = $event"
            @gotArtist="Artist = $event"
            @gotTopTracks="TopTracks = $event"
            ></app-search-bar>
        <br>
        <div v-if="init" id="tracksection" class="row m-auto">
            <div class="col-lg-6 col-md-12 col-sm-12 pt-2">
                <div class="panel col-md-12">
                    <div class="row m-auto pt-3 trackheader">
                        <div class="col-lg-12 col-md-12 col-sm-12">
                            <h2 ><MusicalNotes class="icon"></MusicalNotes> Track: </h2>
                        </div>
                    </div>
                    <div class="row m-auto pt-3">
                        <div class="col-lg-7 col-md-5 col-sm-12">
                            <h4>{{ Track.name }} <span class="explicit" v-if="Track.explicit">EXPLICIT</span> </h4>
                            <h5>
                                <ul id="artistlist" class="p-0">
                                    <li class="genres" v-for="artist in Track.artists" :key="artist.name">{{ artist.name }}</li>
                                </ul>
                            </h5>
                        </div>
                        <div class="col-lg-5 col-md-7 col-sm-12">
                            <iframe :src="src" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
                            
                        </div>
                    </div>
                    <div class="row m-auto pt-3">
                        <div class="col-md-7 col-sm-12 p-0">
                            
                            <div id="chart">
                                <apexchart type=radar height=350 :options="chartOptions" :series="getTrackFeatures" />
                            </div>
                        </div>
                        <div class="col-md-5 col-sm-12">
                            <div class="container p-0">
                                <h5 class="text-center">Stats</h5>
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

            <div class="artist col-lg-6 col-md-12 col-sm-12 pt-2">
               <div class="panel col-md-12">
                   <div class="row m-auto pt-3 trackheader">
                        <div class="col-lg-12 col-md-12 col-sm-12">
                            <h2><Person class="icon"></Person> Artist: </h2>
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
                                <img class="img-fluid shadow " :src="Artist.images ? Artist.images[1].url : ''">
                                <div class="container pt-3">
                                    <h5>Popularity: {{ Artist.popularity }}</h5>
                                    <h5>Followers: {{ Artist.followers ? Number(Artist.followers.total).toLocaleString() : ''}}</h5>
                                    <h5>Genres: </h5>
                                    <ul>
                                        <li class="genres" v-for="genre in Artist.genres" :key="genre">{{ genre }}</li>
                                    </ul>         
                                </div>
                            </div>
                        </div>
                        <div class="col-md-6 col-sm-12">
                            <h5>Top tracks by popularity</h5>
                            <h5>(United States)</h5>
                            <div id="chart2">
                                <apexchart type=bar height=350 :options="getBarGraphOptions" :series="getTopTracks" />
                            </div>
                        </div>
                    </div>
               </div>
            </div>
        </div>

        <div v-if="init" id="chart3" class="row m-auto">
            <div class="col-md-12">
                <h2 class="m-0"><Volume class="icon"></Volume> Track Volume: </h2>
                <apexchart type=area height=300 :options="loudnessOptions" :series="getLoudnessSeries" />
            </div>
        </div>
        
        <div v-if="init" class="row m-auto">
            <div class="col-md-12 col-sm-12">
                <h2><Disc class="icon"></Disc> Album: </h2>
            </div>
        </div>
        <div v-if="init" id="artist" class="row m-auto pt-2 pb-2">
            <div class="col-md-12 col-sm-12">
                <iframe id="albumWidget" :src="playlist_src" width="300" height="390" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
            </div>
        </div>
    </div>
</template>

<script>
import SearchBar from './SearchBar.vue'
import VueApexCharts from 'vue-apexcharts'
import MusicalNotes from 'vue-ionicons/dist/md-musical-notes.vue'
import Disc from 'vue-ionicons/dist/md-disc.vue'
import Person from 'vue-ionicons/dist/md-person.vue'
import Volume from 'vue-ionicons/dist/md-volume-high'
export default {
    data(){
        return{
            init: false,
            src: 'https://open.spotify.com/embed/track/2t8yVaLvJ0RenpXUIAC52d',
            playlist_src: 'https://open.spotify.com/embed/album/',
            TrackID: '',
            Track: {},
            Artist: {},
            TopTracks: {
                tracks: []
            },
            Album: {},
            AlbumUrl: '',
            TrackAnal: {
                track: {
                    key: 0,
                    mode: 0
                }
            },
            TrackFeatures: {},
            chartOptions: {
                labels: ['Acousticness','Energy','Danceability','Instrumentalness','Liveness','Speechiness','Valence'],
                yaxis: {
                    show: false,
                    max: 1,
                    min: 0
                },
                stroke: {
                    colors: ['rgb(54, 199, 110)']
                },
                fill: {
                    colors: ['#36C76E'],
                    opacity: 0.5
                },
                markers: {
                    colors: ['rgb(54, 199, 110)'],
                },
                tooltip:{
                    theme: 'dark'
                },
                chart:{
                    toolbar:{
                        show: false
                    },
                    offsetY: -40
                },
                radar:{
                    polygons:{
                        strokeColors: 'rgb(54, 199, 110)',
                        connectColors: 'rgb(54, 199, 110)'
                    }
                }
            },
            loudness: [],
            loudnessOptions: {
                grid: {
                    yaxis: {
                        lines: {
                            show: false
                        }
                    }
                },
                chart: {
                    stacked: false,
                    zoom: {
                        type: 'x',
                        enabled: true,
                        autoScaleYaxis: true
                    },
                    toolbar: {
                        autoSelected: 'zoom'
                    }
                },
                plotOptions: {
                    line: {
                        curve: 'smooth',
                    }
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    width: 2,
                    colors: ['rgb(54, 199, 110)']
                },
                markers: {
                    size: 0,
                    style: 'full',
                },
                fill: {
                    type: 'solid',
                    opacity: 0
                },
                yaxis: {
                    axisBorder: {
                        show: false
                    },
                    title: {
                        text: 'Loudness (dB)'
                    },
                },
                xaxis: {
                    type: 'numeric',
                    title: {
                        text: 'Time (seconds)'
                    }
                },
                tooltip: {
                    
                }
            },
            
        }
    },
    methods: {
        getLoudness(){
            this.loudness = []
            let i;
            for(i = 0; i < this.TrackAnal.segments.length; i++) {
                var value = [this.TrackAnal.segments[i].start, this.TrackAnal.segments[i].loudness_max];
                this.loudness.push(value);
            }
            //console.log(this.loudness);
        },
    },
    computed:{
        getLoudnessSeries(){
            return [{
                name: 'Loudness',
                data: this.loudness
            }]
        },
        getTrackFeatures(){
            if(Object.keys(this.TrackFeatures).length != 0) {
                return [{
                name: 'Value',
                data: [
                        this.TrackFeatures.acousticness,
                        this.TrackFeatures.energy,
                        this.TrackFeatures.danceability,
                        this.TrackFeatures.instrumentalness,
                        this.TrackFeatures.liveness,
                        this.TrackFeatures.speechiness,
                        this.TrackFeatures.valence]
                }] 
            } else {
                return [{
                    name: 'Value',
                    data: []
                }]
            }
            
        },
        getTopTracks(){
            var toptracks = [];
            var i;
            for(i = 0; i < this.TopTracks.tracks.length; i++){
                toptracks.push(this.TopTracks.tracks[i].popularity)
            }
            return [{
                name: 'Popularity',
                data: toptracks
            }]
        },
        getBarGraphOptions(){
            var toptracknames = [];
            var i;
            for(i = 0; i < this.TopTracks.tracks.length; i++){
                toptracknames.push(this.TopTracks.tracks[i].name)
            }
            return{
                chart:{
                    offsetX: -50,
                    offsetY: -30,
                    toolbar:{
                        show: false
                    }
                },
                colors: ['rgb(54, 199, 110)'],
                grid:{
                    show: false
                },
                markers:{
                    colors:['rgb(20,20,20)']
                },
                plotOptions: {
                    bar: {
                        barHeight: '90%',
                        horizontal: true,
                        dataLabels: {
                            position: 'bottom'
                        },
                        columnWidth: '90%'
                    }
                },
                dataLabels: {
                    enabled: true,
                    textAnchor: 'start',
                    style:{
                        color: ['#fff']
                    },
                    formatter: function (val, opt) {
                        return opt.w.globals.labels[opt.dataPointIndex] + ":  " + val
                    },
                    offsetX: 0,
                    dropShadow: {
                        enabled: true
                    }
                },
                xaxis: {
                    categories: toptracknames,
                    labels:{
                        show: false
                    },
                    axisTicks: {
                        show: false
                    },
                   
                },
                yaxis: {
                    labels: {
                        show: false
                    },
                    min: 0,
                    max: 100
                },
            }
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
            if(Object.keys(this.TrackAnal.length != 0) && typeof this.TrackAnal != 'undefined') {
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
                    default:
                        return ''
                }
            } else {
                return ''
            }
        }
    },
    components:{
        appSearchBar: SearchBar,
        apexchart: VueApexCharts,
        MusicalNotes,
        Disc,
        Person,
        Volume
    },
}
</script>

<style scoped>
    table{
        color:rgb(173, 173, 173)
    }

    h4{
        color: #fff;
    }
    
    h5{
        color: rgb(156, 156, 156);
    }

    h2{
        color: rgb(54, 199, 110);
    }

    ul{
        list-style: none
    }

    td, th{
        padding: 3px;
        font-size: 20px;
    }

    td{
        text-align: right
    }

    .trackheader{
        border-bottom: 1px solid rgb(71, 71, 71);
    }

    .panel{
        background-color: rgb(31, 31, 31);
        border-radius: 0.5rem;
        height: 100%;
    }


    .genres{
        float: left;
        color: rgb(156, 156, 156);
    }

    .genres::after{
        content: ', ';
        white-space: pre;
    }

    .genres:last-child::after{
        content: ''
    }

    .artist img{
        border-radius: 50%;
        height: 60%;
        width: 60%;
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

    .icon{
        vertical-align:text-bottom;
        font-size: 35px;
        display: inline;
        fill: rgb(54, 199, 110);
    }

    iframe{
        width: 100%;
    }


</style>