const { handle } = require('./_lib/http');
module.exports=(req,res)=>handle(req,res,{route:'/api/oauth-callback',publicSafe:false});
