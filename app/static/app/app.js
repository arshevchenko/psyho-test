var psycho = angular.module("psycho", ['ngRoute', 'dndLists']);
var main_title = " - Тестирование";
Array.prototype.shuffle = function(b)
{
 var i = this.length, j, t;
 while( i )
 {
  j = Math.floor( ( i-- ) * Math.random() );
  t = b && typeof this[i].shuffle!=='undefined' ? this[i].shuffle() : this[i];
  this[i] = this[j];
  this[j] = t;
 }
 return this;
};



psycho.config(function($routeProvider, $locationProvider){
  $routeProvider
  .when('/',{
    templateUrl : '/static/view/main.html',
    controller : 'mainCtrl',
    controllerAs: 'main',
    resolve: {
      "check": function($location, UserPerm){
        if(UserPerm.check_access()){
          $location.path("/tests");
        }
      }
    }
  })
  .when('/admin',{
    templateUrl: '/static/view/admin.html',
    controller: 'admPanel',
    controllerAs: 'admin'
  })
  .when('/tests',{
    templateUrl: '/static/view/tests.html',
    controller: 'showTests',
    controllerAs: 'tests',
    resolve: {
      "check_permission": function($location, UserPerm){
        if(!(UserPerm.check_access())){
          $location.path("/");
          console.log(localStorage.getItem('uid'));
        }
       }
    }
  })
  .when('/tests/:id',{
    templateUrl: '/static/view/single_test.html',
    controller: 'showOne',
    controllerAs: 'test'
  })

  .when('/stat',{
    templateUrl: '/static/view/stats.html',
    controller: 'showStats',
    controllerAs: 'stats'
  })

  .when('/last',{
    templateUrl: '/static/view/last.html',
    controller: 'lastStat',
    controllerAs: 'last'
  })

  .otherwise('/');
});

psycho.factory('UserPerm',
  function($location){
    var UserPerm = {};

    UserPerm.log_user = function(uid, id){
      localStorage.setItem("access", true);
      localStorage.setItem("uid", uid);
      localStorage.setItem("id", id);

      $location.path("/tests");
    };

    UserPerm.check_access = function(){
      if(localStorage.getItem("access")){
        return true;
      }else{
        return false;
      }
    };

    return UserPerm;
});

psycho.controller('mainCtrl', mainCtrl);
psycho.controller('admPanel', admPanel);
psycho.controller('showTests', showTests);
psycho.controller('showOne', showOne);
psycho.controller('showStats', showStats);
psycho.controller('lastStat', lastStat);

function mainCtrl($http, $route, $scope, UserPerm){
  $scope.page_title = "Главная" + main_title;

  $scope.send_user = function(form){
      $http.post('/api/login', form)
      .success(function(data){
         UserPerm.log_user(data[0]['uni'], data[0]['id']);
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

function showOne($http, $route, $scope, $routeParams, $interval, $location){
  $scope.time = "00:00:00";
  $scope.hor = 0;
  $scope.sec = 0;
  $scope.min = 0;

  var timerPromise;
  $scope.start = function() {
    timerPromise = $interval(function() {
      $scope.sec = $scope.sec + 1;
      if($scope.sec >= 60) {
        $scope.sec = 0;
        $scope.min = $scope.min + 1;
        if ($scope.min >= 60) {
            $scope.min = 0;
            $scope.hor = $scope.hor + 1;
        }
    }
      $scope.time = ($scope.hor ? ($scope.hor > 9 ? $scope.hor : "0" + $scope.hor) : "00") +
      ":" + ($scope.min ? ($scope.min > 9 ? $scope.min : "0" + $scope.min) : "00") +
      ":" + ($scope.sec > 9 ? $scope.sec  : "0" + $scope.sec );
    }, 1000);
  };

  $scope.stop = function() {
    if (timerPromise) {
      $interval.cancel(timerPromise);
      timerPromise = undefined;
    }
  };

  $scope.reset = function() {
    if (timerPromise) {
      $interval.cancel(timerPromise);
      timerPromise = undefined;
    }
    $scope.min = 0;
    $scope.sec = 0;
    $scope.hor = 0;
  };

  $scope.start();
  $http.get('/api/test/' + $routeParams.id)
        .success(function(data){
          var text_splice = data[0]['text'].split('.');
          var text_prep = [];
          text_splice.splice(text_splice.length - 1, 1);

          for(var i = 0; i < text_splice.length; i++){
            text_prep.push({"pos": i, "text_part": text_splice[i]});
          }

          var saveState = text_prep;
          $scope.test_list = text_prep.shuffle();
          $scope.page_title = data[0]['name'] + main_title;

          $scope.get_positions = function(){
              var err = 0;
              var result_text = "";
              for(var i = 0; i < $scope.test_list.length; i++){
                result_text += $scope.test_list[i]["pos"] + " ";
                if($scope.test_list[i]["pos"] != i){
                  err = err + 1;
                }
              }

              console.log($scope.time);
              console.log(result_text);
              $http.post('/api/stat/' + localStorage.getItem("id"),{
                      "test_id": $routeParams.id,
                      "test_time": $scope.time,
                      "err_count": err,
                      "pos": result_text
                    });
              $location.path("/last");
          }
        });


}

function showStats($http, $route, $scope){
  $scope.page_title = "Ваши результаты" + main_title;
  $http.get('/api/stat/' + localStorage.getItem("id"))
       .success(function(data){
         $scope.test_results = data;
  });
}

function lastStat($http, $route, $scope){
  $http.get('/api/last/' + localStorage.getItem("id"))
       .success(function(data){
         $scope.test_result = data;
         test_ret = function(){
           $location.path("/test/" + data["test_id"]);
         };
  });


}
