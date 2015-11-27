var yamrControllers = angular.module('yamrControllers', []);

yamrControllers.controller('IndexController', ['$scope', 'TopRatedRest', 'RandomRest', 'RatingService', 'SearchRest', 'PosterService',
    function ($scope, TopRatedRest, RandomRest, ratingService, SearchRest, posterService) {

        var fromResponseToScope = function (items){
            items = ratingService.joinRatings(items);
            items = items.map(function(movie){
                movie.poster = posterService.getUrl(movie.tmdbPosterPath, 'M');
                return movie;
            });
            return items;
        };
        $scope.search = function () {
            SearchRest.get({query: $scope.query}, function (response) {
                $scope.searchResults = fromResponseToScope(response.items);
            });
        };
        TopRatedRest.query(function (response) {
            $scope.topRated = fromResponseToScope(response.items);
        });

        RandomRest.get(function (response) {
            $scope.random = fromResponseToScope(response.items);
        });
    }
]);

yamrControllers.controller('MovieDetailController', ['$scope', '$routeParams', 'MovieRest', 'RatingService', 'PosterService',
    function ($scope, $routeParams, MovieRest, ratingService, posterService) {
        MovieRest.get({movieId: $routeParams.movieId}, function (response) {
            var movie = ratingService.joinRatings([response])[0];
            movie.poster = posterService.getUrl(movie.tmdbPosterPath, 'L');
            $scope.movie = movie;
        });
    }
]);

yamrControllers.controller('RatingsController', ['$scope', 'RatingService', 'PosterService',
    function ($scope, ratingService, posterService) {
        $scope.getRatings = function () {
            return ratingService.ratings();
        };

        $scope.addRating = function (movie) {
            console.debug(JSON.stringify(movie));
            ratingService.addRating(movie);
        };

        $scope.getRatingsWithPoster = function(size) {
            var ratings = ratingService.ratings();
            ratings = ratings.map(function(movie){
                movie.poster = posterService.getUrl(movie.tmdbPosterPath, size);
                return movie;
            });
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