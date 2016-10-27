
angular.module('twitApp').controller('homeController', ['$scope', '$http', '$mdDialog', function($scope, $http, $mdDialog) {
		
		//map initialization - code from google maps developer page.
		var links = new google.maps.Data();
		
		var MAP_CENTER = new google.maps.LatLng(11.770570, -2.988281); //position that the main map centers on
		var MINIMUM_ZOOM = 2; //The minimum zoom level a user can zoom out
		var mapOptions = {
			  center: MAP_CENTER,
			  zoom: MINIMUM_ZOOM,
			  mapTypeId: google.maps.MapTypeId.ROADMAP,
			  disableDefaultUI:true,
			  mapTypeControl: true,
			  mapTypeControlOptions: {
				  style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
				  position: google.maps.ControlPosition.TOP_CENTER
			  },
			  streetViewControl: false,
			  streetViewControlOptions: {
				  position: google.maps.ControlPosition.TOP_CENTER
			  }
			};
		$scope.map_canvas = new google.maps.Map(document.getElementById('map_canvas'), mapOptions);
		
		$scope.availableOptions= [{id: '1', name: 'Choose keyword'}, {id: '2', name: 'Obama'}, {id: '3', name: 'Trump'}, {id: '4', name: 'Pogba'}];
		
		/*$http.post("/getTweets", "hello")
		.success(function(data) { //data received in "~" separated values in the form of ["Column chart values"~"Pie chart values for Conventional material"~"Pie chart values for New material"~"Life Cycle Cost of conventional material"~"Life Cycle Cost of New material"]
			console.log(data.status);
 	    })
		.error(function(data) {
            console.log("error");
            console.log(data);
        });*/

		//when user selects a SRI from the dropdown
		 $scope.hasChanged = function() {
			 var keyword = {"key" : $scope.selectedSRI};
			 map_damage = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
			 document.getElementById("map_canvas").style.display = "inline-block";
			 links.setMap(null);
			 links =  new google.maps.Data({map:map_damage});
			 $http.post("/getGeo", keyword)
			 .success(function(data) {
				 var latitudes = JSON.parse(JSON.stringify(data.latitude));
				 var longitudes = JSON.parse(JSON.stringify(data.longitude));
				 var texts = JSON.parse(JSON.stringify(data.text));
				 for(i=0; i<latitudes.length; i++) {
						var position = new google.maps.LatLng(latitudes[i], longitudes[i]);
						var image = new google.maps.MarkerImage(
							'/static/img/twitter.png',
							null,
							null,
							null,
							new google.maps.Size(30, 30));
						
						marker = new google.maps.Marker({
							position: position,
							map: map_damage,
							title: "Tweet"
						});
						marker.setIcon(image);
						var contentString = '<div id = "content">' +
						'<div id="siteNotice">'+
						  '</div>'+
						  '<h4 id="firstHeading" class="firstHeading">' + "Tweet" + '</h4>'+
						  '<div id="bodyContent">'+
						  '<p><b>Text : </b>' + texts[i] + '</p>'+
						  '</div>'+
						  '</div>';

						var infowindow =  new google.maps.InfoWindow({
							content: ''
						});
						bindInfoWindow(marker, map_damage, infowindow, contentString, texts[i]);
					}
					function bindInfoWindow(marker, map, infowindow, html, text) { 
						google.maps.event.addListener(marker, 'mouseover', function() { 
							infowindow.setContent(html); 
							infowindow.open(map, marker); 
						});
						google.maps.event.addListener(marker, 'mouseout', function() { 
							infowindow.close(); 
						});
					}
					
			 })
			 .error(function(data) {
				console.log("error");
				console.log(data);
			 });

			}
		
    }]);

//lccaController - controller for the LCCA.HTML page	- refer to the LCCA.HTML page for further information. (See website - Life Cycle Cost Analysis tab)
	
