var yamrControllers = angular.module('yamrControllers', []);

yamrControllers.controller('IndexController', ['$scope', 'TopRatedRest', 'RandomRest', 'RatingService', 'SearchRest',
    function ($scope, TopRatedRest, RandomRest, ratingService, SearchRest) {

        $scope.search = function () {
            SearchRest.get({query: $scope.query}, function (response) {
                $scope.searchResults = ratingService.joinRatings(response.items);
            });
        };

        TopRatedRest.query(function (response) {
            $scope.topRated = ratingService.joinRatings(response.items);
        });
        RandomRest.get(function (response) {
            $scope.random = ratingService.joinRatings(response.items);
        });
    }
]);

yamrControllers.controller('MovieDetailController', ['$scope', '$routeParams', 'MovieRest', 'RatingService',
    function ($scope, $routeParams, MovieRest, ratingService) {
        MovieRest.get({movieId: $routeParams.movieId}, function (response) {
            $scope.movie = ratingService.joinRatings([response])[0];
            console.debug(JSON.stringify($scope.movie));
        });
    }
]);

yamrControllers.controller('RatingsController', ['$scope', 'RatingService',
    function ($scope, ratingService) {
        $scope.getRatings = function () {
            return ratingService.ratings();
        };

        $scope.addRating = function (movie) {
            console.debug(JSON.stringify(movie));
            ratingService.addRating(movie);
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