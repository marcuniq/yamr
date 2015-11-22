var yamrControllers = angular.module('yamrControllers', []);

yamrControllers.controller('IndexController', ['$scope', 'TopRatedRest',
    function ($scope, TopRatedRest) {
        $scope.topRated = TopRatedRest.query();
    }
]);

yamrControllers.controller('MovieDetailController', ['$scope', '$routeParams', 'MovieRest',
    function ($scope, $routeParams, MovieRest) {
        $scope.movie = MovieRest.get({movieId: $routeParams.movieId}, function (movie) {
            $scope.poster = movie.poster;
        });
    }
]);