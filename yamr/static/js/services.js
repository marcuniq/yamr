// Module specific configuration
angular.module('yamrServices.config', [])
    .value('yamrServices.config', {
        basePath: '/', //http://private-66bc5-yamr.apiary-mock.com/' // Set your base path here
        posterMediumPath: 'http://image.tmdb.org/t/p/w185',
        posterLargePath: 'http://image.tmdb.org/t/p/w342'
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

yamrServices.factory('RandomRest', ['$resource', 'yamrServices.config',
    function ($resource, config) {
        return $resource(config.basePath + 'api/movies/random');
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
    function ($localStorage) {
        var ratingService = this;
        if ($localStorage.ratings === undefined) {
            $localStorage.ratings = [];
        }

        var find_by_id = function (movieId) {
            return function (element, index, array) {
                return element.movieId == movieId;
            };
        };

        return {
            ratings: function () {
                // This exposed private data
                return $localStorage.ratings;
            },
            addRating: function (movie) {
                // This is a public function that modifies private data
                var ratedMovie = $localStorage.ratings.find(find_by_id(movie.movieId));
                if (ratedMovie != undefined) {
                    ratingService.deleteRating(movie.movieId);
                }
                movie.ratingTimestamp = new Date().getTime();
                $localStorage.ratings.push(movie);
            },
            deleteRating: function (movieId) {
                // This is a public function that modifies private data
                $localStorage.ratings = $localStorage.ratings.filter(function (el) {
                    return el.movieId != movieId;
                });
            },
            joinRatings: function (unratedMovies) {
                return unratedMovies.map(function (movie) {
                    var ratedMovie = $localStorage.ratings.find(find_by_id(movie.movieId));
                    if (ratedMovie != undefined) {
                        movie.rating = ratedMovie.rating;
                    }
                    return movie;
                });
            }
        };
    }
);

yamrServices.factory('PosterService', ['yamrServices.config',
    function(config) {
        return {
            getUrl: function(imgPath, size){
                if (size == 'L')
                    return config.posterLargePath + imgPath;
                else
                    return config.posterMediumPath + imgPath;
            }
        };
    }
]);