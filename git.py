import os
import subprocess


URL_GITHUB = 'https://github.com/{repo}/{path}.git'
URL_GITLAB = 'https://gitlab-new.{repo}/{path}.git'

 
class Git:

    BASE_URL = URL_GITHUB

    def __init__(self, path: str, repo: str=''):
        if not os.path.exists(path):
            self.clone(self.BASE_URL.format(repo=repo, path=path))
        os.chdir(path)
        self.new_branch = ''
        
    def run(self, command: str) -> list:
        print('**', command, '===============')
        result = subprocess.run(command, capture_output=True, text=True)
        return str(result.stdout).split('\n')

    def clone(self, url: str):
        self.run('git clone ' + url)

    def pull(self):
        self.run('git pull')

    def push(self):
        option = ''
        if self.new_branch:
            option = f' --set-upstream origin {self.new_branch}'
        self.run('git push'+option)

    def add(self, param: str):
        self.run(f'git add {param}')

    def commit(self, message: str, add_all: bool = True):
        if add_all:
            self.add('--all')
        self.run(f'git commit -m "{message}"')

    def checkout(self, branch: str, check_branch: bool=True):
        option = ''
        if check_branch and branch not in self.branch():
            option = '-b'
            self.new_branch = branch
        command = f'git checkout {option} {branch}'
        self.run(command)

    def branch(self) -> list:
        return [
            b.replace('*', '').strip()
            for b in self.run('git branch') if b
        ]

    def diff(self, extension='.py') -> dict:
        result = {}
        for line in self.run('git diff'):
            if line.endswith(extension):
                file_name = line.split('/')[-1]
            elif line and line[0] in '+-':
                result.setdefault(file_name, []).append(line)
        return result


# ====== Exemplo de como usar ... ============================
def exemplo():
    """
    Fluxo de trabalho: 
        * Pegar uma tarefa, 
        * Baixar o repo,
        * Fazer as alterações, 
        * Testar
        * Subir de volta para o repositório
    """
    print('Você deseja...?')
    print('(I)niciar um desenvolvimento')
    print('(F)inalizar um desenvolvimento')
    op = input('Escolha sua opção: ')
    git = Git('Aprendendo_GIT', 'juliocascalles')
    if op in ('i', 'I'):
        TAREFA = 'A001' # <<--- Como seria no JIRA, por exemplo...
        git.checkout(TAREFA, check_branch=True)
        git.pull() # <<---- Pega alterações de outros programadores
    elif op in ('f', 'F'):
        NOVO_RECURSO = "[feat] Fiz exemplo de como usar git"
        CORRECAO_BUG = "[fix] Não estava funcionando..."
        DOCUMENTACAO = "[doc] Novo README.md do projeto!"
        git.commit(NOVO_RECURSO)
        git.push()
# ============================================================


if __name__ == '__main__':
    exemplo()
