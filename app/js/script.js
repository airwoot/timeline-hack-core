var theirTimeline = angular.module('theirTimeline',[]);
theirTimeline.controller('login',['$scope','$http', function($scope, $http) {
        $scope.logged = false
        $scope.login = function(){
            url = "http://timeline-hack.cloudapp.net/twitter_auth"
            $http.get(url).success(function(data, status, headers, config) {
            console.log(url)
            $scope.logged = true
            })
        }
        $scope.search = function(){
        url = 'http://api.gaana.com/index.php?type=search&subtype=search_song&content_filter=2&key='+$scope.query
        console.log('temp')
        $http.get(url).success(function(data, status, headers, config) {
            console.log(url)
            console.log(data)
            $scope.tracks = data['tracks']
            
            })
        
        }
        $scope.download2 = function(track_id, album_id, seokey){
            trackb64 = btoa(track_id)
            hmac = CryptoJS.HmacMD5(trackb64, 'ec9b7c7122ffeed819dc1831af42ea8f');
            song_url_get_url = 'http://api.gaana.com/getURLV1.php?quality=medium&album_id='+album_id+'&delivery_type=stream&hashcode='+hmac+'&isrc=0&type=rtmp&track_id='+track_id
            var config = {headers : {
                'deviceType' : 'GaanaAndroidApp',
                'appVersion' : 'V5'
            
            }}
            console.log(song_url_get_url)
                $http.get(song_url_get_url, config).success(function(data, status, headers, config){
                download_url = atob(data['data'])
                
                        })
            .error(function (data, status, headers, config) {
                      alert("error");
                            return status;
                    
                    })
            if(download_url.indexOf('mp3') > -1){
                $scope.durl = download_url
                $scope.filename = seokey+'.mp3'
                console.log($scope.filename)
          console.log(download_url)
         
            }   
            else{
                $scope.durl = download_url
                $scope.filename = seokey+'.mp3'
          
            }
          $scope.hidden = false;
        
        }
        $scope.download = function(track_id, album_id, seokey){
            trackb64 = btoa(track_id)
            hmac = CryptoJS.HmacMD5(trackb64, 'ec9b7c7122ffeed819dc1831af42ea8f');
            song_url_get_url = 'http://api.gaana.com/getURLV1.php?quality=medium&album_id='+album_id+'&delivery_type=stream&hashcode='+hmac+'&isrc=0&type=rtmp&track_id='+track_id
                var config = {headers : {
                'deviceType' : 'GaanaAndroidApp',
                'appVersion' : 'V5'
            
                }}
            console.log(song_url_get_url)
                $http.get(song_url_get_url, config).success(function(data, status, headers, config){
                download_url = atob(data['data'])
                console.log('Download Url Got')
                console.log(download_url)
                
                        })
            .error(function (data, status, headers, config) {
                      alert("error");
                            return status;
                    
                    })
            if(download_url.indexOf('mp3') > -1){
                console.log('Downloading Mp3')
                console.log(download_url)
                var blob = new Blob(['Hello World'],{type:"text/plain;charset=utf-8"});
                $http.get(download_url)
                    .success(function(data, status){
                        console.log(status) 
                        var file = new Blob([data], {type : "audio/mp3"});
                        console.log(file)
                        console.log(seokey+'.mp3')
                        window.saveAs(file, seokey+'.mp3')
                        console.log(seokey+'.mp3')
                            
                            })
            
            }
            else{
                console.log('Downloading Mp4')
                console.log(download_url)
                var blob = new Blob(['Hello World'],{type:"text/plain;charset=utf-8"});
                window.saveAs(blob, '/Users/tushar/Download/helloworld.txt')
                $http.get(download_url)
                .success(function(data){
                        console.log(status) 
                        var file = new Blob([data], {type : "video/mp4"});
                        console.log(file)
                        console.log(seokey+'.mp4')
                        saveAs(file, seokey+'.mp4')
                        console.log(seokey+'.mp4')
                            
                        })
            
            }
        
        }
        
        }]
        )

