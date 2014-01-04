def cdeditor_set(id, *options):
    import simplejson as sj
    
    argument = "%r" % id
    if options:
        argument += ',' + sj.dumps(options[0])

    return """<script type="text/javascript">
	window.onload = function()
	{
		CKEDITOR.replace( %s );
	};
</script>
""" % argument

def call(app, var, env):
    
    env['ckeditor_set'] = cdeditor_set
    return {'toplinks':[
        '{{=url_for_static("ckeditor/ckeditor.js")}}',
        ]}

