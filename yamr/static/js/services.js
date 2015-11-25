// Module specific configuration
angular.module('yamrServices.config', [])
    .value('yamrServices.config', {
        basePath: '/' //http://private-66bc5-yamr.apiary-mock.com/' // Set your base path here
    });

var yamrServices = angular.module('yamrServices', ['ngResource', 'yamrServices.config', 'ngStorage']);

yamrServices.factory('MovieRest', ['$resource', 'yamrServices.config',
    function ($resource, config) {
        return $resource(config.basePath + 'api/movies/:movieId', {});
    }
]);

yamrServices.factory('TopRatedRest', ['$resource', 'yamrServices.config',
    function ($resource, config) {
        return $resource(config.basePath + 'api/movies/top_rated', {}, {
            query: {method: 'GET', isArray: false}
        });
    }
]);

yamrServices.factory('SearchRest', ['$resource', 'yamrServices.config',
    function ($resource, config) {
        return $resource(config.basePath + 'api/search', {}, {
            query: {method: 'GET', params: {query: ''}, isArray: true}
        });
    }
]);

yamrServices.factory('RecommenderRest', ['$resource', 'yamrServices.config',
    function ($resource, config) {
        return $resource(config.basePath + 'api/recommend', {}, {
            query: {method: 'POST', params: {movieId: ''}, isArray: true}
        });
    }
]);

yamrServices.factory('RatingService',
    function($localStorage){
        if ($localStorage.ratings === undefined) {
            $localStorage.ratings = [];
        }

        return {
            ratings:function () {
                // This exposed private data
                return $localStorage.ratings;
            },
            addRating:function (movie) {
                // This is a public function that modifies private data
                $localStorage.ratings.push(movie);
            },
            deleteRating:function (movieId) {
                // This is a public function that modifies private data
                $localStorage.ratings = $localStorage.ratings.filter(function(el){
                    return el.movieId != movieId;
                });
            }
        };
    }
);