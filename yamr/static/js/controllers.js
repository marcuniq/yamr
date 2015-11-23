var yamrControllers = angular.module('yamrControllers', []);

yamrControllers.controller('IndexController', ['$scope', 'TopRatedRest',
    function ($scope, TopRatedRest) {
        TopRatedRest.query(function(response){
            $scope.topRated = response.items;
        });
    }
]);

yamrControllers.controller('MovieDetailController', ['$scope', '$routeParams', 'MovieRest',
    function ($scope, $routeParams, MovieRest) {
        $scope.movie = MovieRest.get({movieId: $routeParams.movieId});
    }
]);