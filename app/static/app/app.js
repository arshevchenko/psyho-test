var psycho = angular.module("psycho", ["ngRoute"]);

psycho.config(function($routeProvider){
  $routeProvider
  .when('/',{
    templateUrl : 'static/view/main.html',
    controller : 'mainCtrl',
    controllerAs: 'main'
  });
});

psycho.controller('mainCtrl', mainCtrl);

function mainCtrl($http, $route, $scope){
  $scope.page_title = "Главная";
  $http.get('/api/test')
       .success(function(data){
         $scope.json_data = data;
       });
}
