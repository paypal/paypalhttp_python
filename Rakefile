require 'rake'

task :default => :test

task :release => [:clean, :test, :release_braintreehttp]

task :test do
  sh "nosetests"
end

task :clean do
  sh "rm -rf dist"
end

task :release_braintreehttp do
  sh "python setup.py sdist bdist_wheel --universal"
  sh "twine upload dist/*"
end
