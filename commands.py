import click
import os
import subprocess as sp
import shutil

#github globals
username = 'xdavio'

@click.group()
def cli():
    """
    All jcc commands.
    """
    pass

@click.command()
@click.argument('folder')
@click.option('--doctype', '-t', type = click.Choice(['reg','slides', 'lec']), default = 'reg', help = 'Select the option of the type of LaTeX document you wish to create.')
def tex(folder, doctype):
    """
    Copies the latex template from the package tex library into a file called document.tex within [folder].
    """
    import pkg_resources
    resource_package = __name__  ## Could be any module/package name.
    resource_path = os.path.join('tex', doctype, 'document.tex')
    #template = pkg_resources.resource_string(resource_package, resource_path)

    if not os.path.exists(folder):
        os.makedirs(folder)

    shutil.copyfile(resource_path, os.path.join(folder, 'document.tex'))

cli.add_command(tex)


@click.command()
def clean():
    """
    Remove backups of the form *~
    """
    os.system('rm *~')

cli.add_command(clean)


@click.group()
def g():
    """
    Git subcommand.
    """
    pass

cli.add_command(g)


@click.command()
@click.argument('reponame')
def init(reponame):
    """
    Create a new github repository named [REPONAME]. Make sure that you create the REPO on github.com first. 
    """
    if not os.path.exists('.git'):
        os.system("echo \"\# " + reponame + "\" >> README.md")
        os.system("git init")
        os.system("git add README.md")
        os.system("git commit -m \"first commit\"")
        os.system("git remote add origin git@github.com:" + username + "/" + reponame + ".git")
        os.system("git push -u origin master")
    else:
        click.echo("The .git directory already exists.")
        if click.confirm("Do you wish to delete it?"):
            shutil.rmtree('.git')

g.add_command(init)


@click.command()
@click.argument('msg')
def cp(msg):
    """
    Commit and push.
    """
    cmd = ['git', 'status', '--porcelain']
    proc = sp.Popen(cmd,stdout=sp.PIPE)
    #for line in iter(proc.stdout.readline,''):
    to_commit = []
    to_add = []
    for line in proc.stdout:
        note = line[1]
        fo = line[2:].rstrip()
        if note == 'M':
            to_commit.append(fo)
        elif note == '?' and fo != '.gitignore':
            to_add.append(fo)
    print to_add
    print to_commit

    if to_add:
        os.system('git add ' + ' '.join(to_add))
        os.system('git commit ' + ' '.join(to_add) + ' -m ' + msg)

    if to_commit:
        os.system('git commit ' + ' '.join(to_commit) + ' -m ' + msg)

    if to_commit or to_add:
        os.system('git push')
    
    #os.system('git add *')
    #os.system('git commit')

g.add_command(cp)


@click.command()
@click.argument('addlines', nargs = -1)
def ignore(addlines):
    """
    Generate .gitignore. Add as many [ADDLINES] as needed; append these to .gitignore.
    """
    if not os.path.exists('.gitignore'):
        click.echo("No .gitignore detected. Writing a default which excludes backups and the 'venv' directory.")
        with open('.gitignore', 'w') as fo:
            fo.write('venv\n')
            fo.write('*~\n')
            fo.write('*pyc\n')
            for line in addlines:
                fo.write(line + '\n')

    else:
        click.echo(".gitignore already exists.")
        if click.confirm("Do you wish to delete it?"):
            os.system("rm .gitignore")

    click.echo("Printing .gitignore...")
    os.system('cat .gitignore')

g.add_command(ignore)





#
# @click.group()
## def ve():
##     """
##     Virtual Environment commands
##     """
##     pass
## cli.add_command(ve)

## @click.command()
## def a():
##     """
##     Doesn't actually activate the virtual environment. Assumes that you're in a directory with
##     /venv/bin/activate
##     available to it. Prints the command for easy use.
##     """
##     click.echo('source venv/bin/activate')

## ve.add_command(a)


## @click.command()
## def d():
##     """
##     Deactivates the virtual environment.
##     """
##     sp.call('deactivate', shell = True)

## ve.add_command(d)
