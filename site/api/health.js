const { handle } = require('./_lib/http');
module.exports=(req,res)=>handle(req,res,'/api/health');
