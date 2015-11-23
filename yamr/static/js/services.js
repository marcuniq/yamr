// Module specific configuration
angular.module('yamrServices.config', [])
    .value('yamrServices.config', {
        basePath: 'http://private-66bc5-yamr.apiary-mock.com/' // Set your base path here
    });

var yamrServices = angular.module('yamrServices', ['ngResource', 'yamrServices.config']);

yamrServices.factory('MovieRest', ['$resource', 'yamrServices.config',
    function ($resource, config) {
        return $resource(config.basePath + 'movies/:movieId', {});
    }
]);

yamrServices.factory('TopRatedRest', ['$resource', 'yamrServices.config',
    function ($resource, config) {
        return $resource(config.basePath + 'movies/top_rated', {}, {
            query: {method: 'GET', isArray: false}
        });
    }
]);

yamrServices.factory('SearchRest', ['$resource', 'yamrServices.config',
    function ($resource, config) {
        return $resource(config.basePath + 'search', {}, {
            query: {method: 'GET', params: {query: ''}, isArray: true}
        });
    }
]);

yamrServices.factory('RecommenderRest', ['$resource', 'yamrServices.config',
    function ($resource, config) {
        return $resource(config.basePath + 'recommend', {}, {
            query: {method: 'POST', params: {movieId: ''}, isArray: true}
        });
    }
]);