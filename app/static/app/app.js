var psycho = angular.module("psycho", ["ngRoute"]);
var main_title = " - Тестирование";

psycho.config(function($routeProvider, $locationProvider){
  $routeProvider
  .when('/',{
    templateUrl : '/static/view/main.html',
    controller : 'mainCtrl',
    controllerAs: 'main'
  })
  .when('/admin',{
    templateUrl: '/static/view/admin.html',
    controller: 'admPanel',
    controllerAs: 'admin'
  })
  .when('/tests',{
    templateUrl: '/static/view/tests.html',
    controller: 'showTests',
    controllerAs: 'tests'
  })
  .when('/tests/:id',{
    templateUrl: '/static/view/single_test.html',
    controller: 'showOne',
    controllerAs: 'test'
  })
  .otherwise('/');

  $locationProvider.html5Mode(true);
});

psycho.controller('mainCtrl', mainCtrl);
psycho.controller('admPanel', admPanel);
psycho.controller('showTests', showTests);
psycho.controller('showOne', showOne);

function mainCtrl($http, $route, $scope, $location){
  $scope.page_title = "Главная" + main_title;

  $scope.send_user = function(form){
      $http.post('/api/login', form)
      .success(function(data){
          console.log(data["uid"]);
          $location.path("tests");

      });
  }
}

function admPanel($http, $route, $scope){
  $scope.page_title = "Панель администрирования" + main_title;

  $scope.send_new_test = function(form){
    $http.post('/api/admin', form)
         .success(function(data){
           console.log(data);
         });
  }
}

function showTests($http, $route, $scope){
  $scope.page_title = "Тесты" + main_title;

  $http.get('/api/test')
        .success(function(data){
          $scope.test_list = data;
        });

}

function showOne($http, $route, $scope, $routeParams){
  $http.get('/api/test/' + $routeParams.id)
        .success(function(data){
          $scope.test_params = data[0];
          $scope.page_title = data[0]['name'] + main_title;
        });
}
