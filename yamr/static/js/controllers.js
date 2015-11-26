var yamrControllers = angular.module('yamrControllers', []);

yamrControllers.controller('IndexController', ['$scope', 'TopRatedRest','RandomRest','RatingService', 'SearchRest',
    function ($scope, TopRatedRest, RandomRest, ratingService, SearchRest) {

        $scope.search = function() {

            SearchRest.get({query: $scope.query}, function(response){
                $scope.searchResults = response.items;
                console.debug(response);
            });
        }

        TopRatedRest.query(function(response){
            $scope.topRated = response.items;
        });
        RandomRest.get(function(response){
            $scope.random = response.items;
        });
        $scope.getRatings = function(){
            return ratingService.ratings();
        }

        $scope.addRating = function(movie) {
            console.debug('add rating');
            ratingService.addRating(movie);
        };
    }
]);

yamrControllers.controller('MovieDetailController', ['$scope', '$routeParams', 'MovieRest',
    function ($scope, $routeParams, MovieRest) {
        $scope.movie = MovieRest.get({movieId: $routeParams.movieId});
    }
]);

yamrControllers.controller('RatingsController', ['$scope', 'RatingService',
    function($scope, ratingService){
        $scope.getRatings = function(){
            return ratingService.ratings();
        };

        $scope.addRating = function(movie) {
            ratingService.addRating(movie);
        };
    }
]);