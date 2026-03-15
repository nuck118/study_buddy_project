Pod::Spec.new do |s|
  s.name        = 'ReactAppDependencyProvider'
  s.version     = '1.0.0'
  s.summary     = 'Local stub for ReactAppDependencyProvider to satisfy CocoaPods during local builds'
  s.license     = 'MIT'
  s.author      = { 'Local' => 'local' }
  s.platforms   = { :ios => '11.0' }
  s.source      = { :path => '.' }
  s.source_files = 'ReactAppDependencyProvider/**/*.{h,m,swift}'
  s.public_header_files = 'ReactAppDependencyProvider/**/*.h'
end
