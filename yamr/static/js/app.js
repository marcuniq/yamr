var yamrApp = angular.module('yamrApp', ['ngRoute', 'ngResource', 'yamrControllers', 'yamrServices', 'angular.filter', 'ui.bootstrap']);

yamrApp.config(['$routeProvider',
    function ($routeProvider) {
        $routeProvider.
        when('/', {
            templateUrl: 'static/partials/landing.html',
            controller: 'IndexController'
        }).
        when('/movies/:movieId', {
            templateUrl: 'static/partials/movie-detail.html',
            controller: 'MovieDetailController'
        }).
        when('/ratings', {
            templateUrl: 'static/partials/ratings.html',
            controller: 'RatingsController'
        }).
        when('/recommendations', {
            templateUrl: 'static/partials/recommendations.html',
            controller: 'RecommendController'
        }).
        when('/about', {
            templateUrl: 'static/partials/about.html',
            controller: 'RatingsController'
        }).
        otherwise({
            redirectTo: '/'
        });
    }
]);

yamrApp.config(['$resourceProvider',
    function ($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }
]);

yamrApp.config(function ($sceDelegateProvider) {
    $sceDelegateProvider.resourceUrlWhitelist([
        // Allow same origin resource loads.
        'self',
        // Allow loading from our assets domain.  Notice the difference between * and **.
        'http://srv*.assets.example.com/**',
        'http*://www.youtube.com/**',
        'http://image.tmdb.org/**'
    ]);

    // The blacklist overrides the whitelist so the open redirect here is blocked.
    $sceDelegateProvider.resourceUrlBlacklist([
        //'http://myapp.example.com/clickThru**'
    ]);
});