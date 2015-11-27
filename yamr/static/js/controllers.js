var yamrControllers = angular.module('yamrControllers', []);

yamrControllers.controller('IndexController', ['$scope', 'TopRatedRest', 'RandomRest', 'SearchRest', 'ResponseConverterService',
    function ($scope, TopRatedRest, RandomRest, SearchRest, responseConverter) {
        $scope.search = function () {
            SearchRest.get({query: $scope.query}, function (response) {
                $scope.searchResults = responseConverter.convert(response.items, 'M');
            });
        };
        TopRatedRest.query(function (response) {
            $scope.topRated = responseConverter.convert(response.items, 'M');
        });

        RandomRest.get(function (response) {
            $scope.random = responseConverter.convert(response.items, 'M0');
        });
    }
]);

yamrControllers.controller('MovieDetailController', ['$scope', '$routeParams', 'MovieRest', 'ResponseConverterService',
    function ($scope, $routeParams, MovieRest, responseConverter) {
        MovieRest.get({movieId: $routeParams.movieId}, function (response) {
            var movie = responseConverter.convert([response], 'L')[0];
            $scope.movie = movie;
        });
    }
]);

yamrControllers.controller('RatingsController', ['$scope', 'RatingService', 'ResponseConverterService',
    function ($scope, ratingService, responseConverter) {
        $scope.getRatings = function () {
            return ratingService.ratings();
        };

        $scope.addRating = function (movie) {
            console.debug(JSON.stringify(movie));
            ratingService.addRating(movie);
        };

        $scope.getRatingsWithPoster = function(size) {
            var ratings = responseConverter.convert(ratingService.ratings(), size);
            return ratings;
        };


        $scope.max = 5;
        $scope.isReadonly = false;

        $scope.hoveringOver = function (value) {
            $scope.overStar = value;
            $scope.percent = 100 * (value / $scope.max);
        };

        $scope.ratingStates = [
            {stateOn: 'glyphicon-ok-sign', stateOff: 'glyphicon-ok-circle'},
            {stateOn: 'glyphicon-star', stateOff: 'glyphicon-star-empty'},
            {stateOn: 'glyphicon-heart', stateOff: 'glyphicon-ban-circle'},
            {stateOn: 'glyphicon-heart'},
            {stateOff: 'glyphicon-off'}
        ];
    }
]);

yamrControllers.controller('RecommendController', ['$scope', 'RecommenderRest', 'RatingService', 'ResponseConverterService',
    function($scope, recommenderRest, ratingService, responseConverter){

        var movieRatings = ratingService.ratings().map(function(movie){
            return {movieId: movie.movieId, rating: movie.rating};
        });

        recommenderRest.query({ratings: movieRatings}, function(response){
            $scope.recommendations = responseConverter.convert(response.items, 'M');
        });
    }
]);